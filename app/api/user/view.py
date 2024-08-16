from flask import Blueprint, request
from flask_login import login_required

from app.util.code import ResponseCode
from app.util.exception import handle_errors
from app.api.user import control as ctl
from app.util.response import ResMsg

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'], endpoint='login')
@login_required
@handle_errors('登录')
def login():
    """
    登录
    :return:
    """
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    success = ctl.login(username, password)
    if success:
        return ResMsg(code=ResponseCode.Success, msg='登录成功').data

    return ResMsg(code=ResponseCode.Fail, msg='登录失败').data
