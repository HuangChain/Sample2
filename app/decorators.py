# coding:utf-8
from functools import wraps
from flask import abort
from flask_login import current_user

from .models import Permission


# 带参数的装饰器，如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数
# 执行顺序:permission_required(permission),返回decorator函数，调用decorator(f),最终返回值decorated_function
def permission_required(permission):
    def decorator(f):
        @wraps(f)  # 把原始函数的__name__等属性复制到wrapper()函数中
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)  # 如果用户不具有指定权限,则返回403错误码,即 HTTP“禁止”错误
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

