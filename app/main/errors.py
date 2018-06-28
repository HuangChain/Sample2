# coding:utf-8
# 蓝本中的错误处理程序
from flask import render_template, request, jsonify
from . import main
"""
在蓝本中编写错误处理程序稍有不同,如果使用 errorhandler 修饰器,那么只有蓝本中的
错误才能触发处理程序。要想注册程序全局的错误处理程序,必须使用 app_errorhandler
"""


@main.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        # 检查Accept请求首部,Werkzeug将其解码为request.accept_imetypes,根据首部的值决定客户端期望接收的响应格式
        # 浏览器一般不限制响应的格式，所以只为接受JSON格式而不接受HTML格式的客户端生成JSON格式响应
        response = jsonify({'error': 'not found'})
        # jsonify将我们传入的json形式数据序列化成为json字符串,作为响应的body,并且设置响应的Content-Type为application/json,构造出响应返回至客户端
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

