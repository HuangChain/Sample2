#!/usr/bin/env python
# coding:utf-8
# 用于启动程序以及其他的程序任务
"""
Shebang这个符号通常在Unix系统的脚本中第一行开头中写到它指明了执行这个脚本文件的解释程序,
所以在基于 Unix 的操作系统中可以通过 ./manage. py 执行脚本,而不用使用复杂的 python manage.py
"""
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


"""
manager.command 修饰器让自定义命令变得简单。修饰函数名就是命令名,函数的文档字符串会显示在帮助消息中,
test() 函数的定义体中调用了 unittest 包提供的测试运行函数
"""


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# length 选项可以修改报告中显示的函数数量
# profile-dir 选项,每条请求的分析数据就会保存到指定目录下的一个文件中
@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run(debug=True)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Role
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()

