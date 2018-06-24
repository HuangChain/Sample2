# coding:utf-8
# 蓝本中定义的程序路由
from datetime import datetime
from flask import render_template, abort, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required

from . import main
from ..models import User, Role, Post, Permission
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
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
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        # current_user由Flask - Login提供, 和所有上下文变量一样, 也是通过线程内的代理对象实现。这个对象的表现类似用户对象,
        # 但实际上却是一个轻度包装, 包含真正的用户对象。 数据库需要真正的用户对象, 因此要调用_get_current_object()方法
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)  # 默认第一页，参数type=int保证参数无法转换成整数时,返回默认值
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=2,
        error_out=False)  # 为True时(默认值),如果请求的页数超出了范围,则会返回404错误;为False,页数超出范围时会返回一个空列表
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,pagination=pagination)


@main.route('/user/<username>')  # 资料页面的路由
def user(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=2,
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)


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
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)  # 用户由id指定,因此可使用Flask-SQLAlchemy提供的get_or_404()函数,如果id不正确,则会返回404错误
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.name.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.name.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

