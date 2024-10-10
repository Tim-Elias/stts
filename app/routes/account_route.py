from flask import Blueprint, render_template, jsonify, request, session, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.openai.transcription import transcribe_audio
from app.openai.analyze_text import analyze_text
from app.routes.forms import AudioForm
import os
 # Импортируем логгер

account_bp = Blueprint('account', __name__)


@account_bp.route('/account', methods=['GET'])
def account():
    current_app.logger.info("Отображение страницы аккаунта.")
    return render_template('account.html')


@account_bp.route('/protected', methods=['GET'])
@jwt_required()  # Требуется авторизация с JWT
def protected():
    current_user = get_jwt_identity()
    current_app.logger.info(f"Запрос защищенного ресурса от пользователя: {current_user}")
    return jsonify(logged_in_as=current_user), 200


@account_bp.route('/get_username', methods=['GET'])
@jwt_required()  # Требуется авторизация с JWT
def get_username():
    current_user = get_jwt_identity()
    from app.database.managers.user_manager import UserManager
    # Создаем экземпляр менеджера базы данных
    db = UserManager()
    current_app.logger.info(f"Запрос имени пользователя от пользователя: {current_user}")
    user=db.get_user_by_user_id(current_user)
    username=user.username
    current_app.logger.info(f"Получено имя пользователя: {username}")
    return jsonify(username), 200