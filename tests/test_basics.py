# coding:utf-8
import unittest
from flask import current_app
from app import create_app, db
"""
setUp() 方法尝试创建一个测试环境,类似于运行中的程序。首先,使用测试配置创建程序,
然后激活上下文。这一步的作用是确保能在测试中使用 current_app,像普通请求一 样。
然后创建一个全新的数据库,以备不时之需。数据库和程序上下文在 tearDown() 方法 中删除
"""


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 第一个测试确保程序实例存在
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    # 第二个测试确保程序在测试配置中运行
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

