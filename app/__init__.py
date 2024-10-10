from flask import Flask
from flask_jwt_extended import JWTManager
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from app.database import init_db, set_db_globals
from app.s3 import init_s3_manager
from app.database.migrations.admin import admin
from app.routes import register_routes
from app.openai import init_openai
from app.logger import init_logger  # Импортируем логгер

load_dotenv()

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    

    init_logger(app)
    app.logger.info("Создание экземпляра приложения Flask.")
    app.logger.info("Инициализация логгера.")

    # Настройки приложения
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        app.logger.info("Настройки приложения загружены.")
    except Exception as e:
        app.logger.error(f"Ошибка при загрузке настроек приложения: {e}")
        raise

    # Настройка JWT
    try:
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Секретный ключ для JWT
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Время истечения токена доступа
        jwt = JWTManager(app)
        app.logger.info("JWT инициализирован.")
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации JWT: {e}")
        raise

    # Настройка OpenAI
    try:
        app.config['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
        app.logger.info("Настройки OpenAI загружены.")
    except Exception as e:
        app.logger.error(f"Ошибка при загрузке настроек OpenAI: {e}")
        raise
    
    # Настройка хранилища s3
    try:
        app.config['endpoint_url']=os.getenv('ENDPOINT_URL')
        app.config['region_name']=os.getenv('REGION_NAME')
        app.config['aws_access_key_id']=os.getenv('AWS_ACCESS_KEY_ID')
        app.config['aws_secret_access_key']=os.getenv('AWS_SECRET_ACCESS_KEY')
        app.config['bucket_name']=os.getenv('BUCKET_NAME')
        app.logger.info("Настройки s3 хранилища загружены.")
    except Exception as e:
        app.logger.error(f"Ошибка при загрузке настроек s3 хранилища: {e}")
        raise

    login = os.getenv('LOGIN')
    password = os.getenv('PASSWORD')

    # Настройка Google OAuth
    try:
        google = oauth.register(
            name='google',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_params=None,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
            client_kwargs={'scope': 'openid email profile'},
        )
        app.logger.info("Google OAuth инициализирован.")
    except Exception as e:
        app.logger.error(f"Ошибка при регистрации Google OAuth: {e}")
        raise

    # Инициализация базы данных
    try:
        engine, Session, Base = init_db(app)
        set_db_globals(engine, Session, Base)
        #admin('admin', 'admin', 'admin')
        app.logger.info("База данных успешно инициализирована.")
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise

    # Инициализация OpenAI
    try:
        init_openai(app)
        app.logger.info("OpenAI успешно инициализирован.")
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации OpenAI: {e}")
        raise

    # Инициализация s3
    try:
        init_s3_manager(app)
        app.logger.info("s3 хранилище успешно инициализировано.")
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации s3 хранилища: {e}")
        raise

    # Регистрация маршрутов
    try:
        register_routes(app)
        app.logger.info("Маршруты успешно зарегистрированы.")
    except Exception as e:
        app.logger.error(f"Ошибка при регистрации маршрутов: {e}")
        raise

    # Регистрация маршрутов Google Auth
    from app.routes import google_auth_bp  # Обновите путь к вашим модулям
    app.register_blueprint(google_auth_bp)
    google_auth_bp.oauth = google
    app.logger.info("Маршрут Google Auth успешно зарегистрирован.")

    return app