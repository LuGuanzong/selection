from flask_login import login_user

from app.api.user import common as c


def login(username: str, password: str) -> bool:
    """
    判断用户名和密码是否匹配
    :param username: 用户名
    :param password: 密码
    :return: 如果匹配，就返回True
    """
    user = c.judge_login(username, password)
    if user:
        login_user(user)
        return True

    return False
