# coding:utf-8
# 蓝本中定义的程序路由
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
"""
在蓝本中编写视图函数主要有两点不同:
1.和前面的错误处理程序一样,路由修饰器 由蓝本提供;
2.url_for() 函数的用法不同:
Flask 会为蓝本中的全部端点加上一个命名空间,这样就可以在不
同的蓝本中使用相同的端点名定义视图函数,而不会产生冲突。
命名空间就是蓝本的名字(Blueprint构造函数的第一个参数),所以视图函数index()注册的端点名是main.index,
其URL使用url_for('main.index')获取,该函数还支持一种简写的端点形式,在蓝本中可以省略蓝本名
"""


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。
# @app.route('/secret')
# @login_required
# def secret():
#     return "only authenticated users are allowed!"
