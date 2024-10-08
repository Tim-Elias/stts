from flask import Blueprint, render_template, jsonify, request, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.openai.transcription import transcribe_audio
from app.openai.analyze_text import analyze_text
from urllib.parse import quote, unquote
from app.routes.forms import AudioForm
import logging
# Получаем логгер по его имени
logger = logging.getLogger('chatbot')


transcription_bp = Blueprint('transcription', __name__)


@transcription_bp.route('/transcription', methods=['GET'])
def transcription():
    form = AudioForm()
    return render_template('transcription.html', form=form)



@transcription_bp.route('/transcription_result', methods=['GET'])
def transcription_result():
    return render_template('transcription_result.html')

@transcription_bp.route('/process_audio', methods=['POST'])
@jwt_required()  # Убедитесь, что пользователь аутентифицирован
def process_audio():
    from app.database.managers.transcription_manager import TranscriptionManager
    db = TranscriptionManager()
    from app.database.managers.audio_manager import AudioFileManager
    db_a = AudioFileManager()
    prompt = request.form.get('prompt_name')
    audio_file = request.files.get('audio')
    current_user = get_jwt_identity()
    logger.info(f"Получен файл: {audio_file}, prompt: {prompt}", extra={'user_id': current_user})
    # Проверка на отсутствие файла или подсказки
    if not audio_file or not prompt:
        logger.warning("Отсутствует аудиофайл или подсказка.", extra={'user_id': current_user})
        return jsonify({'msg': 'Missing audio file or prompt.'}), 400
    
    # Декодируем имя файла, если это необходимо
    filename = audio_file.filename  # Декодируем имя файла
    #file_extension = os.path.splitext(filename)[1]
    file_record = db_a.get_audio_file_by_name(current_user, filename)
    file_extension = file_record.file_extension
    logger.info(f"Получен файл: {filename}, расширение: {file_extension}", extra={'user_id': current_user})

    audio_bytes = audio_file.read()  # Преобразуем FileStorage в байты

    try:
        logger.info("Начало транскрибации аудио.", extra={'user_id': current_user})
        transcription = transcribe_audio(audio_bytes, file_extension)
        logger.info("Транскрибация завершена.")
        
        logger.info("Анализ текста.", extra={'user_id': current_user})
        analysis, tokens = analyze_text(prompt, transcription)

        logger.info(f"Сохранение транскрипции для пользователя: {current_user}", extra={'user_id': current_user})
        transcription_id = db.add_transcription(current_user, filename, transcription, analysis, prompt, tokens)
        return jsonify({"transcription_id": transcription_id})
        """return jsonify({
            'transcription': transcription,
            'analysis': analysis,
            'filename': filename
        }), 200"""
    except Exception as e:
        logger.error(f"Ошибка в процессе обработки аудио: {e}", extra={'user_id': current_user})
        return jsonify({'msg': 'Error processing audio.'}), 500

@transcription_bp.route('/result', methods=['GET'])
def result():
    transcription = request.args.get('transcription')
    analysis = request.args.get('analysis')
    return render_template('result.html', transcription=transcription, analysis=analysis)

@transcription_bp.route('/transcriptions', methods=['GET'])
@jwt_required()
def get_transcriptions():
    from app.database.managers.transcription_manager import TranscriptionManager
    db = TranscriptionManager()
    current_user = get_jwt_identity()
    offset = request.args.get('offset', default=0, type=int)  # Получаем offset из параметров запроса
    limit = request.args.get('limit', default=10, type=int)  # Получаем limit из параметров запроса
    logger.info(f"Запрос транскрипций для пользователя: {current_user} с offset={offset} и limit={limit}", extra={'user_id': current_user})
    transcriptions = db.get_transcription_by_user(current_user, offset, limit)
    
    if transcriptions:
        logger.info("Транскрипции найдены.", extra={'user_id': current_user})
        return jsonify(transcriptions), 200
    else:
        logger.warning("Транскрипции не найдены.", extra={'user_id': current_user})
        return jsonify({"msg": "No transcriptions found"}), 404




@transcription_bp.route('/api/transcription/<transcription_id>', methods=['GET'])
@jwt_required()
def get_transcription_by_transcription_id(transcription_id):
    current_user = get_jwt_identity()
    logger.info(f"Запрос на получение транскрипции по transcription_id: {transcription_id} для пользователя: {current_user}", extra={'user_id': current_user})
    from app.database.managers.transcription_manager import TranscriptionManager
    
    db = TranscriptionManager()
    transcription = db.get_transcription_by_id(transcription_id)

    if transcription:
        return jsonify({
            'transcription_id': transcription.transcription_id,  # Убедитесь, что это поле существует
            'text': transcription.text,
            'analysis': transcription.analysis,
            'prompt': transcription.prompt,
            'tokens': transcription.tokens
        }), 200
    else:
        logger.warning("Транскрипция не найдена.", extra={'user_id': current_user})
        return jsonify({"msg": "Transcription not found"}), 404



@transcription_bp.route('/transcription/view/<transcription_id>', methods=['GET'])
def view_transcription_page(transcription_id):
    from app.database.managers.transcription_manager import TranscriptionManager
    db = TranscriptionManager()
    transcription = db.get_transcription_by_id(transcription_id)
    if transcription:
        return render_template('transcription_details.html', transcription=transcription)
    else:
        return "Транскрипция не найдена", 404




@transcription_bp.route('/user_prompts', methods=['GET'])
@jwt_required()
def get_user_prompts():
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    current_user = get_jwt_identity()
    
    logger.info(f"Запрос готовых промптов для пользователя: {current_user}", extra={'user_id': current_user})
    prompts = prompt_manager.get_prompts_by_user(current_user)  # Извлекаем промпты для текущего пользователя
    prompt_data = []
    for s in prompts:
        prompt_info = {
            "prompt_name": s[0]
        }
        
        prompt_data.append(prompt_info)
    if prompt_data:
        return jsonify(prompt_data=prompt_data), 200
    else:
        return jsonify({"msg": "No prompts found"}), 404


@transcription_bp.route('/user_audio_files', methods=['GET'])
@jwt_required()
def get_user_audio_files():
    from app.database.managers.audio_manager import AudioFileManager
    audio_manager = AudioFileManager()
    current_user = get_jwt_identity()
    logger.info(f"Запрос аудиофайлов для пользователя: {current_user}", extra={'user_id': current_user})
    audio_files = audio_manager.get_audio_files_by_user(current_user)

    if audio_files:
        logger.info("Аудиофайлы найдены.", extra={'user_id': current_user})
        return jsonify(audio_files=audio_files), 200
    else:
        logger.warning("Аудиофайлы не найдены.", extra={'user_id': current_user})
        return jsonify({"msg": "No audio files found"}), 404



@transcription_bp.route('/get_automatic_prompt', methods=['GET'])
@jwt_required()
def get_automatic_prompt():
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    current_user = get_jwt_identity()

    # Получаем автоматический промпт
    automatic_prompt = prompt_manager.get_automatic_prompt(current_user)

    if automatic_prompt:
        logger.info(f"Автоматический промпт найден и отправлен пользователю {current_user}", extra={'user_id': current_user})
        return jsonify(automatic_prompt), 200  # Возвращаем полные данные о промпте
    else:
        return jsonify({"msg": "No automatic prompt found"}), 404


