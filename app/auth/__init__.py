# coding:utf-8
"""
创建程序的过程移入工厂函数后,可以使用蓝本在全局作用 域中定义路由。
与用户认证系统相关的路由可在 auth 蓝本中定义。
对于不同的程序功能, 我们要使用不同的蓝本,这是保持代码整齐有序的好方法
蓝本的包构造文件创建蓝本对象,再从 views.py 模块 中引入路由
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views