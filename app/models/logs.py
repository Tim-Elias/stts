from app.database.db_setup import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=False)  # ID пользователя, совершившего действие
    action = Column(String(255), nullable=False)    # Действие, которое было выполнено
    message = Column(String(255), nullable=False)   # Сообщение лога
    timestamp = Column(DateTime, default=datetime.utcnow)  # Дата и время

    def to_dict(self):
        """Преобразование объекта лога в словарь."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "message": self.message,
            "timestamp": self.timestamp.isoformat()  # Форматируем дату для JSON
        }
