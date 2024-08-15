from app.model.sql.user import User
from app.util.exception import UserException


def judge_login(username: str, password: str) -> User | None:
    """
    判断用户名和密码是否匹配
    :param username: 用户名
    :param password: 密码
    :return: 验证成功就返回用户信息
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        raise UserException('当前用户不存在')

    if not password or user.password != password:
        raise UserException('当前账户密码不匹配')

    return user
