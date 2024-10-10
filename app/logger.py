import logging
from logging.handlers import RotatingFileHandler

# Настройка логирования
"""logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)"""


# Настройка логирования
handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

def init_logger(app):
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)