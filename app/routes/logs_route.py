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


@logs_bp.route('/api/logs', methods=['GET'])
@jwt_required()
def get_logs():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    from app.database.managers.logs_manager import LogManager
    log_manager = LogManager()
    logs, total_count = log_manager.get_logs(user_id=user_id, date=date, offset=offset, limit=limit)

    return jsonify({'total': total_count, 'logs': logs})  # Убедитесь, что возвращаете правильный формат
