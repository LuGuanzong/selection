import logging
import logging.config as logging_config
import os

from flask import Flask
import yaml

from app.api import hello_world_bp
from app.extension.db import db
from app.api.product import product_bp


def create_app(config_name):
    app = Flask(__name__)

    # 加载配置文件
    load_config(app, config_name)

    # 加载插件
    load_extensions(app)

    # 注册蓝图
    load_blueprints(app)

    return app


def load_config(app: Flask, config_name='DEVELOPMENT'):
    """
    加载配置文件
    :param config_name: 当前配置环境
    :param app: Flask实例
    """
    pwd = os.getcwd()
    config_path = os.path.join(pwd, 'config/config.yaml')
    if not config_name:
        config_name = 'DEVELOPMENT'

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)


def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')


def load_extensions(app: Flask):
    """
    加载插件
    :param app: app
    :return:
    """
    db.init_app(app)


def load_blueprints(app: Flask):
    """
    加载蓝图
    :param app: 框架实例
    """
    app.register_blueprint(hello_world_bp)
    app.register_blueprint(product_bp)


def load_logging(app: Flask):
    # 日志文件目录
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])

    # 日志设置
    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging_config.dictConfig(dict_conf)
