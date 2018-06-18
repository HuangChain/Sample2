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


if __name__ == '__main__':
    manager.run()