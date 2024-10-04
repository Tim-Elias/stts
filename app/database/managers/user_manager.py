from sqlalchemy import exists
from app.models.user import User  
from app.database.db_globals import Session

class UserManager:
    def __init__(self):
        self.Session = Session

    def add_user_password(self, username, user_id, password, auth_type='password', user_type='user'):
        """Добавляем пользователя стандартно"""
        session = self.Session()
        new_user = User(username=username, user_id=user_id, auth_type=auth_type, user_type=user_type)
        new_user.set_password(password)  # Устанавливаем хэш пароля
        session.add(new_user)
        session.commit()
        session.close()

    def check_password(self, username, password):
        """Проверяем пароль пользователя"""
        session = self.Session()
        user = session.query(User).filter_by(user_id=username).first()
        session.close()
        if user and user.check_password(password):
            return True
        return False

    def update_user_password(self, username, new_password):
        """Обновляем пароль пользователя"""
        session = self.Session()
        user = session.query(User).filter_by(user_id=username).first()
        if user:
            user.set_password(new_password)  # Обновляем хэш пароля
            session.commit()
        session.close()

    def add_user_google(self, username, email, auth_type='google', user_type='user'):
        """Добавляем пользователя через google"""
        session = self.Session()
        new_user = User(username=username, user_id=email, auth_type=auth_type, user_type=user_type)
        session.add(new_user)
        session.commit()
        session.close()

    def user_exists(self, user_id):
        """Проверка существования пользователя по имени"""
        session = self.Session()
        exists_query = session.query(exists().where(User.user_id == user_id)).scalar()
        session.close()
        return exists_query
    
    def google_user_exists(self, user_id):
        """Проверка существования пользователя по имени"""
        session = self.Session()
        exists_query = session.query(exists().where(User.user_id == user_id)).scalar()
        session.close()
        return exists_query
    
    def get_user_by_user_id(self, user_id):
        """Получить пользователя по google_id"""
        session = self.Session()
        try:
            # Получаем пользователя по id
            user = session.query(User).filter_by(user_id=user_id).first()
        finally:
            # Закрываем сессию в блоке finally, чтобы гарантировать закрытие независимо от результата запроса
            session.close()

        # Возвращаем найденного пользователя или None, если не найдено
        return user