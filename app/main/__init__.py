# coding:utf-8
from flask import Blueprint


"""
蓝本和程序类似,也可以定义路由,在蓝本中定义的路由处于休眠状态,直到蓝本注册到程序上后,路由才真正成为程序 的一部分
通过实例化一个 Blueprint 类对象可以创建蓝本。这个构造函数有两个必须指定的参数: 
蓝本的名字和蓝本所在的包或模块。和程序一样,大多数情况下第二个参数使用 Python 的 __name__ 变量即可
"""
main = Blueprint('main', __name__)

from . import views, errors  # 避免循环导入依赖,因为在views.py和errors.py中还要导入蓝本 main。