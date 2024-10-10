from sqlalchemy import exists
from app.models.prompt import Prompt
import uuid
from app.database.db_globals import Session
from flask import current_app

class PromptManager:
    def __init__(self):
        self.Session = Session

    def add_prompt(self, user, prompt_name, text, use_automatic=False):
        session = self.Session()
        current_app.logger.info("Сохранение промпта в базу данных.")
        prompt_id = uuid.uuid4()
        new_prompt = Prompt(prompt_id=prompt_id, user=user, prompt_name=prompt_name, text=text, use_automatic=use_automatic)
        session.add(new_prompt)
        session.commit()
        session.close()
        current_app.logger.info("Промпт успешно сохранен.")

    def get_prompts_by_user(self, user):
        session = self.Session()
        try:
            current_app.logger.info(f"Получение промптов для пользователя: {user}")
            prompts = session.query(Prompt).filter_by(user=user).all()
            result = [[p.prompt_name, p.text, p.prompt_id, p.use_automatic] for p in prompts]
        finally:
            session.close()
        return result
    
    def get_prompt_by_prompt_id(self,  prompt_id):
        session = self.Session()
        try:
            current_app.logger.info(f"Получение промпта по prompt_id: {prompt_id}")
            prompt = session.query(Prompt).filter_by( prompt_id=prompt_id).first()


        finally:
            session.close()
        return prompt

    def get_prompt_by_prompt_name(self, user, prompt_name):
        session = self.Session()
        try:
            current_app.logger.info(f"Получение промпта по prompt_id: {prompt_name}")
            prompt = session.query(Prompt).filter_by(user=user, prompt_name=prompt_name).first()
        finally:
            session.close()
        return prompt

    def edit_prompt(self, prompt_id, new_text, new_prompt_name):
        session = self.Session()
        try:
            current_app.logger.info(f"Редактирование промпта '{prompt_id}'")
            prompt = session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                prompt.text = new_text
                prompt.prompt_name = new_prompt_name  # Обновляем имя промпта
                session.commit()
                current_app.logger.info(f"Промпт '{prompt_id}' обновлен ")
                return True  # Успешное редактирование
            else:
                current_app.logger.warning(f"Промпт '{prompt_id}' не найден")
                return False  # Промпт не найден
        except Exception as e:
            current_app.logger.error(f"Ошибка при редактировании промпта: {e}")
            session.rollback()
            raise e
        finally:
            session.close()



    def delete_prompt(self, prompt_id):
        session = self.Session()
        try:
            current_app.logger.info(f"Удаление промпта '{prompt_id}'")
            prompt = session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                session.delete(prompt)
                session.commit()
                current_app.logger.info(f"Промпт '{prompt_id}' успешно удален.")
            else:
                current_app.logger.warning(f"Промпт '{prompt_id}' не найден")
        except Exception as e:
            current_app.logger.error(f"Ошибка при удалении промпта: {e}")
            session.rollback()
            raise e
        finally:
            session.close()


    def get_automatic_prompt(self, user):
        session = self.Session()
        try:
            current_app.logger.info(f"Поиск автоматического промпта для пользователя: {user}")
            prompt = session.query(Prompt).filter_by(user=user, use_automatic=True).first()  # Получаем первый промпт с флагом use_automatic=True
            
            # Возвращаем всю информацию о промпте, если он найден
            if prompt:
                current_app.logger.info(f"Автоматический промпт '{prompt.prompt_name}' найден для пользователя: {user}")
                return {
                    "prompt_name": prompt.prompt_name,
                    "text": prompt.text,
                    "prompt_id": prompt.prompt_id,
                    "use_automatic": prompt.use_automatic
                }
            else:
                current_app.logger.info(f"Автоматический промпт не найден для пользователя: {user}")
                return None
        except Exception as e:
            current_app.logger.error(f"Ошибка при поиске автоматического промпта: {e}")
            raise e
        finally:
            session.close()



        

    def reset_automatic_flag(self, user):
        current_app.logger.info(f"Сброс флага 'use_automatic' для всех промптов пользователя {user}.")
        session = self.Session()
        try:
            prompts = session.query(Prompt).filter_by(user=user, use_automatic=True).all()
            for prompt in prompts:
                prompt.use_automatic = False
            session.commit() 
            current_app.logger.info(f"Флаг 'use_automatic' сброшен для {len(prompts)} промптов пользователя {user}.")
        except Exception as e:
            current_app.logger.error(f"Ошибка при сбросе флага 'use_automatic' для пользователя {user}: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
            current_app.logger.info(f"Сессия для сброса флагов 'use_automatic' для пользователя {user} закрыта.")


    def set_automatic_flag(self, prompt_id, use_automatic):
        current_app.logger.info(f"Установка флага 'use_automatic' для промпта ID: {prompt_id} на {use_automatic}.")
        session = self.Session()
        try:
            prompt = session.query(Prompt).filter_by(prompt_id=prompt_id).first()
            if prompt:
                prompt.use_automatic = use_automatic
                session.commit()
                current_app.logger.info(f"Флаг 'use_automatic' для промпта ID: {prompt_id} успешно обновлён на {use_automatic}.")
            else:
                current_app.logger.warning(f"Промпт ID: {prompt_id} не найден.")
                raise ValueError(f"Prompt with ID {prompt_id} not found")
        except Exception as e:
            current_app.logger.error(f"Ошибка при установке флага 'use_automatic' для промпта ID: {prompt_id}: {e}")
            session.rollback()
            raise e
        finally:
            session.close()
            current_app.logger.info(f"Сессия для установки флага 'use_automatic' для промпта ID: {prompt_id} закрыта.")
