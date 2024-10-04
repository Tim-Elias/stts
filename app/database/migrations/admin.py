def admin(password, username, user_id):
    from app.database.managers.user_manager import UserManager
    db = UserManager()
    
    #if db.user_exists(username):
        #db.delete_user_by_username(username)

    db.add_user_password(username, user_id, password, user_type='admin')
    print('New admin added successfully')