from app.database.db_setup import Base 
from sqlalchemy import Column, Integer, String, Text

class Transcription(Base):
    __tablename__ = 'transcriptions'

    transcription_id = Column(String, primary_key=True)
    user = Column(String(255), nullable=False)  
    audio_id = Column(String(255), nullable=False)
    text = Column(Text)
    analysis = Column(Text)
    prompt = Column(Text)
    tokens = Column(Integer)