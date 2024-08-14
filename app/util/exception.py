import logging

from app.util.code import ResponseCode
from app.util.response import ResMsg


class UserException(Exception):
    """这是一个可以给用户看到异常信息的异常，或者是程序发现的用户操作失误产生的异常"""

    def __init__(self, message="这是一个自定义的异常"):
        # 调用基类的构造函数
        super().__init__(message)
        self.message = message

    def __str__(self):
        # 返回自定义的异常信息
        return f'【操作错误】{self.message}'


def handle_errors(err_msg):
    """
    用于在视图函数中的总的错误处理
    :param err_msg:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except UserException as e:
                logging.error(f'{err_msg}失败, err: {e}')
                return ResMsg(code=ResponseCode.Fail, msg=f'{err_msg}失败, {e}').data
            except Exception as e:
                logging.error(f'{err_msg}失败, err: {e}')
                return ResMsg(code=ResponseCode.Fail, msg=f'{err_msg}失败, 请咨询管理员').data
        return wrapper
    return decorator
