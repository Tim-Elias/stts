from flask import Blueprint, Response, request, abort, g, current_app, render_template, redirect, jsonify, url_for
from flask import send_file, abort
from flask_jwt_extended import  get_jwt_identity, jwt_required
from functools import wraps



logs_bp = Blueprint('logs', __name__)


@logs_bp.route('/admin_protected', methods=['GET'])
@jwt_required()  # Требуется авторизация с JWT
def admin_protected():
    current_user = get_jwt_identity()
    from app.database.managers.user_manager import UserManager
    db = UserManager()
    
    if not db.is_user_admin(current_user):
        return jsonify({"msg": "Access denied"}), 403
    return jsonify(logged_in_as=current_user), 200


@logs_bp.route('/logs')  
def logs_page():
    return render_template('logs.html')


@logs_bp.route('/logs/data')
@jwt_required() # Применяем ваш декоратор аутентификации
def get_logs_data():
    try:
        with open('app.log', 'r') as log_file:
            logs = log_file.read()
        return jsonify({"logs": logs})
    except Exception as e:
        current_app.logger.error(f"Ошибка при чтении логов: {e}")
        return jsonify({"error": "Error loading logs"}), 500
