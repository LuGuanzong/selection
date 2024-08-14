import os

from flask import Blueprint, current_app, send_from_directory, make_response

hello_world_bp = Blueprint('hello_world', __name__)


# @hello_world_bp.route('/<name>')
@hello_world_bp.route('/')
def hello_world(name=None):
    if name:
        return f'Hello, {name}!'
    else:
        return 'Hello, world!'


@hello_world_bp.route('/download/<filename>', endpoint='download')
def download(filename):
    """
    通过文件名返回资源
    :return:
    """
    filedir = os.path.join(os.getcwd(), current_app.config['UPLOAD_FOLDER'])
    filepath = os.path.join(filedir, filename)

    # 检查文件是否存在
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return make_response('文件未找到', 404)

    return send_from_directory(filedir, filename, as_attachment=True)
