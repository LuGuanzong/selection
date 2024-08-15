from app.api.user import common as c


def judge_login(username: str, password: str) -> bool:
    """
    判断用户名和密码是否匹配
    :param username: 用户名
    :param password: 密码
    :return: 如果匹配，就返回True
    """
    return c.judge_login(username, password)
