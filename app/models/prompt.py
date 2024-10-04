from app.database.db_setup import Base 
from sqlalchemy import Column, Integer, String, Text

class Prompt(Base):
    __tablename__ = 'prompts'

    prompt_id = Column(String, primary_key=True)
    user = Column(String(255), nullable=False)  # Пользователь
    prompt_name = Column(String(255), nullable=False)  # Назвние промпта, чтобы было проще искать
    text = Column(Text)   # Текст промпта