import openai
from app.logger import logger  # Импортируем логгер

def analyze_text(prompt, transcribed_text):
    logger.info("Анализ текста с помощью OpenAI.")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": transcribed_text}]
    )
    analysis = response.choices[0].message.content
    tokens = response.usage.total_tokens
    logger.info("Анализ текста завершен.")
    return analysis, tokens