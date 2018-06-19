# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('password',
                             validators=[DataRequired(message=u"密码不能为空"), Length(2, 10, message=u'长度位于2~10之间')],
                             render_kw={'placeholder': u'输入密码'})
    submit = SubmitField('Submit')