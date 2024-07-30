from flask import Blueprint

hello_world_bp = Blueprint('hello_world', __name__)


@hello_world_bp.route('/<name>')
@hello_world_bp.route('/')
def hello_world(name=None):
    if name:
        return f'Hello, {name}!'
    else:
        return 'Hello, world!'
