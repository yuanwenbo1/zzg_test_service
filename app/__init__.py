# coding: utf-8

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils.Id_servicer import IdWorker
from config import config

db = SQLAlchemy()
id_worker = IdWorker(1, 2, 0)
migrate = Migrate()


def create_app(config_ev="default"):
    '''
    创建flask应用对象
    :param config_ev:
    :return:
    '''
    app = Flask(__name__)
    # 使用配置
    app.config.from_object(config[config_ev])
    # 初始化app
    db.init_app(app)
    migrate.init_app(app, db)
    # 初始化配置
    config.get(config_ev).init_app(app)
    # 设置跨域
    CORS(app, supports_credentials=True)
    # ---蓝图配置---
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    return app
