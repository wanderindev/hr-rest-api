from datetime import datetime
from models.user import AppUserModel


def authenticate(username, password):
    user = AppUserModel.find_by_username(username)
    print(user)
    print(user.is_active)
    print(user.check_password(password))
    if user and user.is_active and user.check_password(password):
        user.login_count += 1
        user.last_login = user.current_login
        user.current_login = datetime.utcnow()
        user.save_to_db()

        return user


def identity(payload):
    return AppUserModel.find_by_id(payload['identity'])
