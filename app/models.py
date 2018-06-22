# coding:utf-8
from . import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request

from datetime import datetime
import hashlib


from .import login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    # 可以直接通过类访问这个方法而不需要创建实例之后才能访问这个方法,它的作用是初始化Role数据表中的数据
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
            }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)  # 注册日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)  # 最后访问日期
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()  # 即role为user的角色

    # 检查用户是否有指定的权限
    # can()方法在请求和赋予角色这两种权限之间进行位与操作。如果角色中包含请求的所有权限位,则返回True,表示允许用户执行此项操作
    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions  # 与结果==permission则说明该角色可以执行此项操作

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    # 刷新用户的最后访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

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

    # 生成一个令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    # 检验令牌，如果检验通过，则把新添加的 confirmed 属性设为 True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        # json里面的字符串都是unicode,loads函数的参数encoding是指定字符串token的编码。
        # 将字符串token读到data时，会按这个编码进行解码成unicode
        except:
            return False
        if data.get('confirm') != self.id:    # self.id为当前用户的id，检查令牌中的id否和存储在current_user中的已登录用户匹配
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username


"""
加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这
个函数必须返回用户对象；否则应该返回 None
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# 将每种权限用一位来表示，0为无权限，1为有权限，一种灵活的权限控制方法
# 可以把这里的十六进制当作二进制看，那么：
# 权限1：0x01 = 0001
# 权限2：0x02 = 0010
# 权限3：0x04 = 0100
# 权限4：0x08 = 1000
# 如果某个用户同时有权限2和4，那么它的权限就是1010；如果有权限123，那么就是0111；如果都有，就是1111；
# 这样来进行权限控制的。用十六进制就是简单的表达二进制
# 0b是说明这段数字是二进制,0x表示是16进制.0x几乎所有的编译器都支持,而支持0b的并不多.


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
