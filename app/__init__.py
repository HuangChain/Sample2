# coding:utf-8
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config, DevelopmentConfig


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
"""
LoginManager 对象的 session_protection 属性可以设为 None、'basic' 或 'strong'，以提
供不同的安全等级防止用户会话遭篡改。设为 'strong' 时，Flask-Login 会记录客户端 IP
地址和浏览器的用户代理信息，如果发现异动就登出用户
"""
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点
login_manager.login_view = 'auth.login'
"""
程序的工厂函数,参数为程序使用的配置名，
配置类在config.py 文件中定义,
其中保存的配置可以使用Flask app.config配置对象提供的from_object()方法直接导入程序
"""


def create_app(config_name):
    app = Flask(__name__)
    # config_name是’default’,等价于app.config.from_object(DevelopmentConfig)
    # 作用就是配置所有的config变量。
    app.config.from_object(config[config_name])
    # app.config.from_object(DevelopmentConfig)
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 蓝本在工厂函数create_app()中注册到程序上
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册蓝本时使用的url_prefix是可选参数。如果使用了这个参数,注册后蓝本中定义的所有路由都会加上指定的前缀
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    # 附加路由和自定义的错误页面

    return app  # 工厂函数返回创建的程序示例