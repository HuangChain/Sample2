# coding:utf-8
import unittest
from app.models import User


#  密码散列化测试
class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    # 测试密码是否能提取
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):u.password

    # 测试是否具有认证密码的功能
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    # 测试不同用户的相同密码的散列值是否相同
    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)