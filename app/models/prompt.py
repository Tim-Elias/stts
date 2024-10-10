from app.database.db_setup import Base 
from sqlalchemy import Column, String, Text, Boolean

class Prompt(Base):
    __tablename__ = 'prompts'

    prompt_id = Column(String, primary_key=True)
    user = Column(String(255), nullable=False)  # Пользователь
    prompt_name = Column(String(255), nullable=False)  # Название промпта
    text = Column(Text)  # Текст промпта
    use_automatic = Column(Boolean, nullable=True, default=False)  # Новый булевый столбец
