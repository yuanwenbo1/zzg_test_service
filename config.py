import logging
import os
# import redis
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'silents is gold'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'
    # celery的redis 配置

    log_path= basedir+"/logs/log"

    @staticmethod
    def init_app(app):
        # 配置日志信息
        # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
        file_log_handler = RotatingFileHandler(Config.log_path, maxBytes=1024 * 1024 * 100, backupCount=10)
        # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
        # 为刚创建的日志记录器设置日志记录格式
        file_log_handler.setFormatter(formatter)
        # 为全局的日志工具对象（flask app使用的）添加日记录器
        logging.getLogger().addHandler(file_log_handler)

        console_log_handler = logging.StreamHandler()
        console_log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_log_handler)
        # 设置日志的记录等级
        logging.basicConfig(level=logging.DEBUG)  # 调试debug级


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

    # 数据库配置
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_dev.db')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:wodeweiyi@127.0.0.1:3306/test_service"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #
    WTF_CSRF_ENABLED = False


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://hsy:4e04.a0mhPBIy%@10.8.17.46:3306/test_service"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'production': Production,
    'default': Production
}
