# coding:utf-8
"""
引入蓝本,然后使用蓝本的 route 修饰器定义与认证相关的路由
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user,  current_user

from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from .. import db
from ..email import send_email


# 对蓝本来说,before_request钩子只能应用到属于蓝本的请求上。若想在蓝本中使用针对程序全局请求的钩子,必须使用before_app_request修饰器
# 在before_app_request处理程序中过滤未确认的账户,同时满足以下3个条件时,before_app_request处理程序会拦截请求
# (1) 用户已登录(current_user.is_authenticated() 必须返回 True)。
# (2) 用户的账户还未确认。
# (3) 请求的端点(使用request.endpoint获取)不在认证蓝本中。访问认证路由要获取权限,因为这些路由的作用是让用户确认账户或执行其他账户管理操作
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth'\
            and request.endpoint != 'static':  # ????????????
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 使用login_user是 将用户标记为已登录状态，后面的jinja2模板中可以使用current_user，
            # 这两个步骤之间就缺乏load_user（）这个回调函数，记录用户的登录状态。
            # 当没有回调函数时，是无法运行login_user()的
            # “记住我”也在表单中填写。如果值为 False，那么关闭浏览器后用户会话就过期了，所以下次用户访问时要重新登录。
            # 如果值为 True，那么会在用户浏览器中写入一个长期有效的 cookie，使用这个 cookie 可以复现用户会话
            login_user(user, form.remember_me.data)
            # 用户访问未授权的URL时会显示登录表单，Flask-Login会把原地址保存在查询字符串的 next 参数中，
            # 这个参数可从 request.args 字典中读取。如果查询字符串中没有 next 参数，则重定向到首页
            next = request.args.get('next')
            if next is None or not next.startswith('/'):  # 用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False
                next = url_for('main.index')
            return redirect(next)
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
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))  # ？？？？？？？跳转到http://127.0.0.1:5000/auth/unconfirmed
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))



@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password')
    return render_template('auth/change_password.html', form=form)


