# coding:utf-8
from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):

    with app.app_context():
        mail.send(msg)


def send_email():
    app = current_app._get_current_object()
    msg = Message(subject="Hello World!",
                  sender='1241908493@qq.com',
                  recipients=["1430250645@qq.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr