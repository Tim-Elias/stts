from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

 # Импортируем логгер

prompt_bp = Blueprint('prompt', __name__)

# Отображение страницы управления промптами
@prompt_bp.route('/manage_prompts', methods=['GET'])
def manage_prompts():
    return render_template('manage_prompts.html')


# Достать все промпты
@prompt_bp.route('/get_prompts', methods=['GET'])
@jwt_required()
def get_prompts():
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    user = get_jwt_identity()
    current_app.logger.info(f"Загрузка страницы управления промптами для пользователя: {user}")
    prompts = prompt_manager.get_prompts_by_user(user)

    prompt_data = []

    for s in prompts:
        prompt_info = {
            "prompt_name": s[0],
            "text": s[1],
            "prompt_id": s[2],
            "use_automatic": s[3]
        }

        current_app.logger.info(f"Загрузка страницы управления промптами для пользователя: {prompt_info}")
        prompt_data.append(prompt_info)

    return jsonify(prompt_data=prompt_data), 200

# Добавление нового промпта
@prompt_bp.route('/add_prompt', methods=['POST'])
@jwt_required()
def add_prompt():
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    user = get_jwt_identity()
    prompt_name = request.form.get('prompt_name')
    text = request.form.get('text')
    try:
        current_app.logger.info(f"Добавление нового промпта для пользователя {user}: Название: {prompt_name}")
        prompt_manager.add_prompt(user, prompt_name, text)
        flash('Prompt added successfully', 'success')
    except Exception as e:
        current_app.logger.error(f"Ошибка при добавлении промпта: {e}")
        flash('An error occurred while adding the prompt', 'danger')
    return jsonify({"message": "Prompt added successfully"}), 200 #redirect(url_for('prompt.manage_prompts'))






# Удаление промпта
@prompt_bp.route('/prompt/<prompt_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_prompt(prompt_id):
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    user = get_jwt_identity()
    try:
        current_app.logger.info(f"Удаление промпта {prompt_id} для пользователя {user}")
        prompt_manager.delete_prompt(prompt_id)
        current_app.logger.info(f"Промпт {prompt_id} удален для пользователя {user}")
        return jsonify(success=True, message='Prompt deleted successfully'), 200
    except Exception as e:
        current_app.logger.error(f"Ошибка при удалении промпта: {e}")
        return jsonify(success=False, message='An error occurred while deleting the prompt'), 500


# Страница добавления нового промпта
@prompt_bp.route('/add_prompts', methods=['GET'])
def add_prompt_page():
    return render_template('add_prompt.html')

# Страница редактирования промпта
@prompt_bp.route('/prompt/<prompt_id>/', methods=['GET'])
def edit_prompt_page(prompt_id):
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    
    prompt = prompt_manager.get_prompt_by_prompt_id(prompt_id)
    
    if prompt:
        return render_template('edit_prompt.html', prompt_id=prompt_id, prompt_name=prompt.prompt_name, prompt_text=prompt.text)
    else:
        flash('Prompt not found', 'danger')
        return redirect(url_for('prompt.manage_prompts'))



# Редактирование существующего промпта
@prompt_bp.route('/prompt/<prompt_id>/edit', methods=['PUT'])
@jwt_required()
def edit_prompt(prompt_id):
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    user = get_jwt_identity()

    data = request.get_json()
    new_text = data.get('text')
    new_prompt_name = data.get('prompt_name')  # Получаем новое имя промпта

    try:
        current_app.logger.info(f"Изменение промпта {prompt_id} для пользователя {user}")
        success = prompt_manager.edit_prompt(prompt_id, new_text, new_prompt_name)  # Передаем новое имя

        if success:
            current_app.logger.info(f"Промпт {prompt_id} изменен для пользователя {user}")
            return jsonify(success=True, message='Prompt updated successfully'), 200
        else:
            current_app.logger.error(f"Промпт {prompt_id} не найден или произошла ошибка")
            return jsonify(success=False, message='Prompt ID not found'), 400

    except Exception as e:
        current_app.logger.error(f"Ошибка при изменении промпта: {e}")
        return jsonify(success=False, message=str(e)), 500


@prompt_bp.route('/prompt/<prompt_id>/set_automatic', methods=['PUT'])
@jwt_required()
def set_automatic(prompt_id):
    from app.database.managers.prompt_manager import PromptManager
    prompt_manager = PromptManager()
    user = get_jwt_identity()

    data = request.get_json()
    use_automatic = data.get('use_automatic')
    current_app.logger.info(f"Запрос на изменение флага 'use_automatic' для промпта {prompt_id} пользователем {user}: {use_automatic}")

    try:
        # Сначала сбрасываем флаг для всех остальных промптов, если устанавливаем новый флаг
        if use_automatic:
            current_app.logger.info(f"Сброс флага 'use_automatic' для всех промптов пользователя {user}.")
            prompt_manager.reset_automatic_flag(user)  # Функция для сброса флага
        # Обновляем выбранный промпт
        prompt_manager.set_automatic_flag(prompt_id, use_automatic)

        current_app.logger.info(f"Флаг 'use_automatic' для промпта {prompt_id} успешно обновлён на {use_automatic}.")
        return jsonify(success=True, message='Automatic flag updated successfully'), 200
    except Exception as e:
        current_app.logger.error(f"Ошибка при изменении флага: {e}")
        return jsonify(success=False, message=str(e)), 500


