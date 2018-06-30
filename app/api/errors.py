# coding:utf-8
from flask import jsonify
from app.exceptions import ValidationError

from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


# 创建一个全局异常处理程序
# 这个修饰器从API蓝本中调用,所以只有当处理蓝本中的路由时抛出了异常才会调用这个处理程序
@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
