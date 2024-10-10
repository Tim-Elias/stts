from sqlalchemy import exists
from app.models.audio import AudioFile
import uuid
from app.database.db_globals import Session
from flask import current_app

class AudioFileManager:
    def __init__(self):
        self.Session = Session

    def add_audio_file(self, user, file_name, file_extension, file_size, bucket_name, s3_key):
        session = self.Session()
        current_app.logger.info(f"Сохранение информации о загруженном аудиофайле '{file_name}' для пользователя '{user}'.")
        audio_id = uuid.uuid4()
        try:
            new_file = AudioFile(
                audio_id=audio_id,
                user=user,
                file_name=file_name,
                file_extension=file_extension,
                file_size=file_size,
                bucket_name=bucket_name,
                s3_key=s3_key
            )
            session.add(new_file)
            session.commit()
            current_app.logger.info(f"Аудиофайл '{file_name}' успешно сохранен в базе данных.")
        except Exception as e:
            current_app.logger.error(f"Ошибка при сохранении аудиофайла '{file_name}': {e}")
            session.rollback()
        finally:
            session.close()

    def get_audio_files_by_user(self, user):
        session = self.Session()
        current_app.logger.info(f"Получение списка аудиофайлов для пользователя '{user}'.")
        try:
            files = session.query(AudioFile).filter_by(user=user).all()
            current_app.logger.info(f"Найдено {len(files)} аудиофайлов для пользователя '{user}'.")
            # Формируем массив массивов
            result = [[f.file_name, f.bucket_name, f.s3_key] for f in files]
            return result
        finally:
            session.close()

    def get_audio_file_by_name(self,user, file_name):
        session = self.Session()
        current_app.logger.info(f"Получение аудиофайла по ID '{file_name}'.")
        try:
            file = session.query(AudioFile).filter_by(user=user, file_name=file_name).first()
            if file:
                current_app.logger.info(f"Аудиофайл '{file.file_name}' найден.")
            else:
                current_app.logger.warning(f"Аудиофайл с ID '{file_name}' не найден.")
            return file
        finally:
            session.close()

    def delete_audio_file(self, audio_id):
        session = self.Session()
        current_app.logger.info(f"Удаление аудиофайла '{audio_id}' из базы данных.")
        try:
            # Найдите файл в базе данных по имени
            file_to_delete = session.query(AudioFile).filter_by(audio_id=audio_id).first()
            if file_to_delete:
                session.delete(file_to_delete)
                session.commit()
                current_app.logger.info(f"Аудиофайл '{audio_id}' успешно удален из базы данных.")
                return True
            else:
                current_app.logger.warning(f"Аудиофайл '{audio_id}' не найден в базе данных.")
                return False
        except Exception as e:
            current_app.logger.error(f"Ошибка при удалении аудиофайла '{audio_id}': {e}")
            session.rollback()
            return False
        finally:
            session.close()