# coding:utf-8
"""
引入蓝本,然后使用蓝本的 route 修饰器定义与认证相关的路由
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user

from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            """
            使用login_user是 将用户标记为已登录状态，后面的jinja2模板中可以使用current_user，
            这两个步骤之间就缺乏load_user（）这个回调函数，记录用户的登录状态。
            当没有回调函数时，是无法运行login_user()的
            """
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)