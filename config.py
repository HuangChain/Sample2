# coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前运行文件路径


class Config:
    SECRET_KEY = 'hard to guess string'
    MAIL_SERVER = 'smtp.qq.com'
    SQLALCHEMY_COMMIT_TEARDOWN = True
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '1241908493@qq.com'
    MAIL_PASSWORD = 'ocvcfuajjxdujbdg'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    """
    配置类可以定义 init_app() 类方法,其参数是程序实例。
    在这个方法中,可以执行对当前 环境的配置初始化
    """
    @staticmethod
    def init_app(app):
        pass


"""
在 3 个子类中,SQLALCHEMY_DATABASE_URI 变量都被指定了不同的值。
这样程序就可在不同 的配置环境中运行,每个环境都使用不同的数据库
"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
    'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):    # ???????????????
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}