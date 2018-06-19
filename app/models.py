# coding:utf-8
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .import login_manager

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # @property装饰器使方法像属性一样调用，就像是一种特殊的属性,方法将变成不可读属性
    # 为了解决对属性的操作，提供了封装方法的方式进行属性的修改,eg:@password.setter
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # @property本身又创建了另一个装饰器@password.setter,负责把一个setter方法变成属性赋值,
    # 计算密码散列值的函数通过名为password的只写属性实现。
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


"""
加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这
个函数必须返回用户对象；否则应该返回 None
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
