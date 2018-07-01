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
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <1241908493@qq.com>'  # 发件人
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True  # 告诉Flask-SQLAlchemy启用记录查询统计数字的功能
    FLASKY_DB_QUERY_TIMEOUT = 0.5  # 缓慢查询的阈值设为0.5秒

    # 配置类可以定义init_app()类方法,其参数是程序实例。在这个方法中,可以执行对当前 环境的配置初始化
    # 返回函数的静态方法,静态方法无需实例化,也可以实例化后调用
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

    # 程序出错时发送电子邮件
    # 普通的方法，第一个参数需要是self，它表示一个具体的实例本身
    # 如果用了staticmethod，那么就可以无视这个self，而将这个方法当成一个普通的函数使用
    # 对于classmethod，它的第一个参数不是self，是cls，它表示这个类本身
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        # 电子邮件日志记录器的日志等级被设为logging.ERROR, 所以只有发生严重错误时才会发送电子邮件
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}