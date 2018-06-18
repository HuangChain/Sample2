# coding:utf-8
from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

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
