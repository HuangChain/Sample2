# coding:utf-8
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
#  g作为flask程序全局的一个临时变量,充当者中间媒介的作用,我们可以通过它传递一些数据
from . import api
from ..models import User
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        # 如果密码为空,那就假定email_or_token参数提供的是令牌,按照令牌的方式进行认证
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False  # 该变量用于区分两种认证方式
    # 如果两个参数都不为空,假定使用常规的邮件地址和密码进行认证
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# 生成认证令牌
# 为了避免客户端使用旧令牌申请新令牌,要在视图函数中检查g.token_used量的值
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})

