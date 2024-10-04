from sqlalchemy import exists
from app.models.transcription import Transcription
import uuid
from app.database.db_globals import Session
from app.logger import logger  # Импортируем логгер

class TranscriptionManager:
    def __init__(self):
        self.Session = Session

    def add_transcription(self, user, audio_id, text, analysis, prompt, tokens):
        session = self.Session()
        logger.info("Сохранение транскрипции в базу данных.")
        transcription_id = uuid.uuid4()
        new_transcription = Transcription(transcription_id=transcription_id,
                                          user=user,
                                           audio_id=audio_id,
                                           text=text,
                                           analysis=analysis,
                                           prompt=prompt,
                                           tokens=tokens)
        session.add(new_transcription)
        session.commit()
        session.close()
        logger.info("Транскрипция успешно сохранена.")
        return transcription_id

    def get_transcription_by_user(self, user, offset=0, limit=10):
        session = self.Session()
        try:
            logger.info(f"Получение транскрипций для пользователя: {user} с ограничением {limit} и смещением {offset}.")
            transcriptions = session.query(Transcription).filter_by(user=user).limit(limit).offset(offset).all()
            result = [{
                'transcription_id': t.transcription_id,  # Добавлено поле transcription_id
                'audio_id': t.audio_id,
                'text': t.text[:100] + '...' if len(t.text) > 100 else t.text,
                'analysis': t.analysis[:100] + '...' if len(t.analysis) > 100 else t.analysis,
                'prompt': t.prompt,
                'tokens': t.tokens
            } for t in transcriptions]
        finally:
            session.close()
        return result



    def get_transcription_by_id(self, transcription_id):
        session = self.Session()
        try:
            logger.info(f"Получение транскрипции по transcription_id: {transcription_id}")
            transcription = session.query(Transcription).filter_by(transcription_id=transcription_id).first()
        finally:
            session.close()
        return transcription



    def get_transcription_by_audio_id(self, user, audio_id):
        session = self.Session()
        try:
            logger.info(f"Получение транскрипции по audio_id: {audio_id}")
            transcription = session.query(Transcription).filter_by(user=user, audio_id=audio_id).first()
            
            if transcription:
                return {
                    'audio_id': transcription.audio_id,
                    'text': transcription.text,
                    'analysis': transcription.analysis,
                    'prompt': transcription.prompt,  # Добавляем prompt
                    'tokens': transcription.tokens   # Добавляем tokens
                }
            else:
                return None  # Если транскрипция не найдена, возвращаем None
        finally:
            session.close()

