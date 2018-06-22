# coding:utf-8
# 蓝本中定义的程序路由
from datetime import datetime
from flask import render_template, abort, flash, redirect, url_for
from flask_login import current_user, login_required

from . import main
from ..models import User
from forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..decorators import admin_required
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

# 资料页面的路由
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    print current_user
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

# 如果未认证的用户访问这个路由，Flask-Login 会拦截请求，把用户发往登录页面。
# @app.route('/secret')
# @login_required
# def secret():
#     return "only authenticated users are allowed!"
