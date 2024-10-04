from sqlalchemy import exists
from app.models.prompt import Prompt
import uuid
from app.database.db_globals import Session
from app.logger import logger  # Импортируем логгер

class PromptManager:
    def __init__(self):
        self.Session = Session

    def add_prompt(self, user, prompt_name, text):
        session = self.Session()
        logger.info("Сохранение промпта в базу данных.")
        prompt_id = uuid.uuid4()
        new_transcription = Prompt(prompt_id=prompt_id, user=user, prompt_name=prompt_name, text=text)
        session.add(new_transcription)
        session.commit()
        session.close()
        logger.info("Промпт успешно сохранен.")

    def get_prompts_by_user(self, user):
        session = self.Session()
        try:
            logger.info(f"Получение промптов для пользователя: {user}")
            prompts = session.query(Prompt).filter_by(user=user).all()
            result = [[p.prompt_name, p.text, p.prompt_id] for p in prompts]
        finally:
            session.close()
        return result
    
    def get_prompt_by_prompt_id(self,  prompt_id):
        session = self.Session()
        try:
            logger.info(f"Получение промпта по prompt_id: {prompt_id}")
            prompt = session.query(Prompt).filter_by( prompt_id=prompt_id).first()


        finally:
            session.close()
        return prompt

    def get_prompt_by_prompt_name(self, user, prompt_name):
        session = self.Session()
        try:
            logger.info(f"Получение промпта по prompt_id: {prompt_name}")
            prompt = session.query(Prompt).filter_by(user=user, prompt_name=prompt_name).first()
        finally:
            session.close()
        return prompt

    def edit_prompt(self, prompt_id, new_text, new_prompt_name):
        session = self.Session()
        try:
            logger.info(f"Редактирование промпта '{prompt_id}'")
            prompt = session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                prompt.text = new_text
                prompt.prompt_name = new_prompt_name  # Обновляем имя промпта
                session.commit()
                logger.info(f"Промпт '{prompt_id}' обновлен ")
                return True  # Успешное редактирование
            else:
                logger.warning(f"Промпт '{prompt_id}' не найден")
                return False  # Промпт не найден
        except Exception as e:
            logger.error(f"Ошибка при редактировании промпта: {e}")
            session.rollback()
            raise e
        finally:
            session.close()



    def delete_prompt(self, prompt_id):
        session = self.Session()
        try:
            logger.info(f"Удаление промпта '{prompt_id}'")
            prompt = session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                session.delete(prompt)
                session.commit()
                logger.info(f"Промпт '{prompt_id}' успешно удален.")
            else:
                logger.warning(f"Промпт '{prompt_id}' не найден")
        except Exception as e:
            logger.error(f"Ошибка при удалении промпта: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

