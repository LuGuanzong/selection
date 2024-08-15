from flask_login import LoginManager

from app.model.sql.user import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)
