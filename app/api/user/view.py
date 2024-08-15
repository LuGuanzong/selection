from flask import Blueprint, request
from flask_login import login_user

from app.util.code import ResponseCode
from app.util.exception import handle_errors
from app.api.user import control as ctl
from app.util.response import ResMsg

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'], endpoint='login')
@handle_errors('登录')
def login():
    """
    登录
    :return:
    """
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    user = ctl.judge_login(username, password)
    if user:
        login_user(user)
        return ResMsg(code=ResponseCode.Success, msg='登录成功')

    return ResMsg(code=ResponseCode.Fail, msg='登录失败')
