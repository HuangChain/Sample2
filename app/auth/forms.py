# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import User


class LoginForm(Form):
    # 电子邮件字段用到了 WTForms 提供的 Length() 和 Email() 验证函数
    email= StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    """确保 username 字段只包含字母、数字、下划线和点号
       正则表达式后面的两个参数分别是正则表达式的旗标和验证失败时显示的错误消息,
       * 表示匹配0个或多个前面这个字符, $匹配一行的结束  
     """
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                        'Usernames must have only letters,'
                                                                                        'numbers, dots or underscores')])
    # EqualTo验证函数要附属到两个密码字段中的一个上，另一个字段则作为参数传入
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    """
    如果表单类中定义了以validate_ 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用,
    自定义的验证函数要想表示验证失败，可以抛出 ValidationError 异常，其参数就是错误消息
    """
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
