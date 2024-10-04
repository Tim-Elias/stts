import openai
from io import BytesIO
from app.logger import logger  # Импортируем логгер


# Класс BytesIO с именем
class NamedBytesIO(BytesIO):
    def __init__(self, initial_bytes, name):
        super().__init__(initial_bytes)
        self.name = name

# Транскрибация аудио
def transcribe_audio(audio, file_format):
    logger.info("Начало транскрибации аудио.")
    audio_file = NamedBytesIO(audio, f"audio.{file_format}")
    audio_file.seek(0)

    try:
        logger.info("Отправка аудио на транскрибацию.")
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ru"
        )
        transcribed_text = response.text
        logger.info("Транскрибация завершена.")
        return transcribed_text
    except Exception as e:
        logger.error(f"Ошибка при транскрибации аудио: {e}")
        raise
    finally:
        audio_file.close()
        logger.info("Закрытие объекта BytesIO.")