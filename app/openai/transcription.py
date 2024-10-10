import openai
from io import BytesIO
from flask import current_app


# Класс BytesIO с именем
class NamedBytesIO(BytesIO):
    def __init__(self, initial_bytes, name):
        super().__init__(initial_bytes)
        self.name = name

# Транскрибация аудио
def transcribe_audio(audio, file_format):
    current_app.logger.info("Начало транскрибации аудио.")
    audio_file = NamedBytesIO(audio, f"audio.{file_format}")
    audio_file.seek(0)

    try:
        current_app.logger.info("Отправка аудио на транскрибацию.")
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="ru"
        )
        transcribed_text = response.text
        current_app.logger.info("Транскрибация завершена.")
        return transcribed_text
    except Exception as e:
        current_app.logger.error(f"Ошибка при транскрибации аудио: {e}")
        raise
    finally:
        audio_file.close()
        current_app.logger.info("Закрытие объекта BytesIO.")