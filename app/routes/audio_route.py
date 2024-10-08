from flask import Blueprint, render_template, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Response, jsonify
import requests
from urllib.parse import quote, unquote
from werkzeug.utils import secure_filename
import os
import logging
# Получаем логгер по его имени
logger = logging.getLogger('chatbot')

audio_bp = Blueprint('audio', __name__)




# Отображение страницы загрузки аудиофайлов
@audio_bp.route('/manage_audio', methods=['GET'])
def manage_audio():
    return render_template('manage_audio.html')


# Загрузка аудиофайла
# Загрузка аудиофайла
@audio_bp.route('/upload_audio', methods=['POST'])
@jwt_required()
def upload_audio():
    from app.database.managers.audio_manager import AudioFileManager
    db = AudioFileManager()
    from app.s3 import get_s3_manager, get_bucket_name
    # Инициализация S3 Manager
    s3_manager = get_s3_manager()
    bucket_name = get_bucket_name()
    current_user = get_jwt_identity()
    logger.info(f"Пользователь {current_user} пытается загрузить аудиофайл.", extra={'user_id': current_user})

    file = request.files.get('file')
    if not file:
        logger.error(f"Пользователь {current_user} не выбрал файл для загрузки.", extra={'user_id': current_user})
        return jsonify({'error': 'No file provided'}), 400

    # Получаем имя файла от пользователя и его расширение
    file_name_input = request.form.get('fileName')  # Имя файла от пользователя
    file_extension = os.path.splitext(file.filename)[1]  # Получаем расширение файла

    # Генерируем полное имя файла с расширением
    full_file_name = f"{file_name_input}{file_extension}"

    # Заменяем пробелы на нижние подчеркивания для s3_key
    s3_key = full_file_name.replace(' ', '_')

    # Получаем размер файла
    file_size = len(file.read())  # Читаем содержимое файла и получаем его размер
    file.seek(0)  # Сбрасываем указатель на начало файла после получения размера

    logger.info(f"Файл для загрузки: {full_file_name}", extra={'user_id': current_user})

    try:
        # Сохраняем временный файл на сервере
        file.save(full_file_name)
        logger.info(f'Попытка загрузить аудио в бакет: {bucket_name}', extra={'user_id': current_user})

        # Загрузка файла в S3
        s3_manager.upload_file(full_file_name, bucket_name, s3_key)  # Используем s3_key с нижними подчеркиваниями
        db.add_audio_file(current_user, file_name_input, file_extension, file_size, bucket_name, s3_key)  # Сохраняем данные в БД
        logger.info(f"Файл {full_file_name} успешно загружен в S3.", extra={'user_id': current_user})

        # Удаляем временный файл после загрузки
        os.remove(full_file_name)

        return jsonify({'message': 'File uploaded successfully'}), 200
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}", extra={'user_id': current_user})
        return jsonify({'error': 'File upload failed'}), 500






# Получение списка файлов с пагинацией
@audio_bp.route('/get_files', methods=['GET'])
@jwt_required()
def get_files():
    from app.database.managers.audio_manager import AudioFileManager
    
    db = AudioFileManager()
    current_user = get_jwt_identity()
    logger.info(f"Пользователь {current_user} запрашивает список файлов.", extra={'user_id': current_user})

    page = int(request.args.get('page', 1))
    per_page = 10

    try:
        # Получаем файлы для текущего пользователя
        files = db.get_audio_files_by_user(current_user)
        total_files = len(files)
        total_pages = (total_files + per_page - 1) // per_page
        
        # Пагинация
        files_paginated = files[(page - 1) * per_page: page * per_page]
        
        file_data = [
            {
                'name': f[0],  # file_name
                's3_key': f[1],  # s3_key
                'bucket_name': f[2]  # bucket_name
            }
            for f in files_paginated
        ]

        logger.info(f"Отправлен список файлов для страницы {page}.", extra={'user_id': current_user})
        return jsonify({'files': file_data, 'total_pages': total_pages}), 200
    except Exception as e:
        logger.error(f"Ошибка при получении списка файлов: {e}", extra={'user_id': current_user})
        return jsonify({'error': 'Failed to retrieve files'}), 500



# Удаление файла
@audio_bp.route('/delete_file', methods=['DELETE'])
@jwt_required()
def delete_file():
    from app.database.managers.audio_manager import AudioFileManager
    db = AudioFileManager()
    from app.s3 import get_s3_manager, get_bucket_name
    current_user = get_jwt_identity()
    file_name = request.json.get('file_name')

    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400

    s3_manager = get_s3_manager()
    bucket_name = get_bucket_name()

    # Проверяем, что файл принадлежит текущему пользователю
    file_record = db.get_audio_file_by_name(current_user, file_name)
    if not file_record:
        return jsonify({'error': 'File not found or access denied'}), 404

    try:
        # Удаляем файл из S3
        s3_manager.delete_file(bucket_name, file_record.s3_key)
        audio_id=file_record.audio_id
        db.delete_audio_file(audio_id)  # Метод для удаления записи из базы
        logger.info(f"Файл {file_name} успешно удален.", extra={'user_id': current_user})
        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Ошибка при удалении файла: {e}", extra={'user_id': current_user})
        return jsonify({'error': 'File deletion failed'}), 500


@audio_bp.route('/download_file_bytes', methods=['GET'])
@jwt_required()
def download_file_bytes():
    from app.database.managers.audio_manager import AudioFileManager
    db = AudioFileManager()
    from app.s3 import get_s3_manager, get_bucket_name
    current_user = get_jwt_identity()
    file_name = request.args.get('file_name')

    logger.info(f"Получен запрос на скачивание файла: {file_name} для пользователя: {current_user}", extra={'user_id': current_user})

    if not file_name:
        logger.warning("Имя файла не указано.", extra={'user_id': current_user})
        return jsonify({'error': 'No file name provided'}), 400

    s3_manager = get_s3_manager()
    bucket_name = get_bucket_name()

    # Проверяем, что файл принадлежит текущему пользователю
    file_record = db.get_audio_file_by_name(current_user, file_name)
    if not file_record:
        logger.warning(f"Файл '{file_name}' не найден или доступ запрещен для пользователя '{current_user}'.", extra={'user_id': current_user})
        return jsonify({'error': 'File not found or access denied'}), 404

    try:
        # Получаем файл из S3
        audio_bytes = s3_manager.get_file(bucket_name, file_record.s3_key)
        if audio_bytes is None:
            logger.error(f"Не удалось получить содержимое файла '{file_name}' из S3.", extra={'user_id': current_user})
            return jsonify({'error': 'Could not retrieve audio file'}), 500
        
        return Response(audio_bytes, mimetype='audio/mpeg')  # Укажите корректный тип контента
    except Exception as e:
        logger.error(f"Ошибка при получении аудиофайла '{file_name}' из S3: {str(e)}", extra={'user_id': current_user})
        return jsonify({'error': f'Could not retrieve audio file: {str(e)}'}), 500


@audio_bp.route('/download_file', methods=['GET'])
@jwt_required()
def download_file():
    from app.database.managers.audio_manager import AudioFileManager
    db = AudioFileManager()
    from app.s3 import get_s3_manager, get_bucket_name
    current_user = get_jwt_identity()
    file_name = request.args.get('file_name')

    if not file_name:
        return jsonify({'error': 'No file name provided'}), 400

    s3_manager = get_s3_manager()
    bucket_name = get_bucket_name()

    # Проверяем, что файл принадлежит текущему пользователю
    # Предполагаем, что `db.get_audio_file_by_user` возвращает объект файла или None
    file_record = db.get_audio_file_by_name(current_user, file_name)
    if not file_record:
        return jsonify({'error': 'File not found or access denied'}), 404

    # Генерируем временный URL для скачивания файла
    url = s3_manager.generate_presigned_url(bucket_name, file_record.s3_key)

    if url:
        return jsonify({'url': url}), 200
    else:
        return jsonify({'error': 'Could not generate download URL'}), 500


