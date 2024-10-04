from flask import Blueprint
from flask_jwt_extended import create_access_token
from flask import render_template, jsonify, request, session



login_bp = Blueprint('login', __name__)


# Основная страница
@login_bp.route('/')
def index():
    return render_template('home.html')


# Маршрут для входа (авторизации)
@login_bp.route('/auth', methods=['POST'])
def auth():
    from app.database.managers.user_manager import UserManager
    # Создаем экземпляр менеджера базы данных
    db = UserManager()
    user_id = request.json.get("user_id", None)
    password = request.json.get("password", None)

    # Проверяем пользователя в базе данных
    if not db.user_exists(user_id) or not db.check_password(user_id, password):
        return jsonify({"msg": "Bad login or password"}), 401

    # Генерируем JWT токен
    access_token = create_access_token(identity=user_id)
    session['access_token'] = access_token  # Сохраняем токен в сессии
    return jsonify(access_token=access_token), 200


# Маршрут для страницы входа
@login_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# Выход из системы
@login_bp.route('/logout')
def logout():
    return jsonify({"msg": "Logout successful"}), 200


@login_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app.database.managers.user_manager import UserManager
    # Создаем экземпляр менеджера базы данных
    db = UserManager()
    if request.method == 'POST':
        username = request.json.get('username', None)
        user_id = request.json.get('user_id', None)
        password = request.json.get('password', None)

        if not user_id or not password:
            return jsonify({"msg": "Login and password are required"}), 400

        if db.user_exists(user_id):
            return jsonify({"msg": "Login already taken"}), 400

        db.add_user_password(username, user_id, password, auth_type='password')

         # Генерируем JWT токен
        access_token = create_access_token(identity=user_id)
        session['access_token'] = access_token  # Сохраняем токен в сессии
        return jsonify(access_token=access_token), 200
    
    if request.method=='GET':
        return render_template('register.html')