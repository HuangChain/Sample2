# coding:utf-8
"""
引入蓝本,然后使用蓝本的 route 修饰器定义与认证相关的路由
"""
from flask import render_template

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')