#!/usr/bin/env python
# encoding: utf-8
import os
import unittest

from src.sign import MtSignClass


class TestSign(unittest.TestCase):
    def test_init(self):
        mt = MtSignClass('username_test', 'password_test')
        self.assertEqual(mt.username, 'username_test')
        self.assertEqual(mt.password, 'password_test')

        for i in ('USERNAME', 'PASSWORD'):
            old = os.environ.get(i)
            os.environ[i] = ''
            with self.assertRaises(ValueError):
                MtSignClass()
            if old:
                os.environ[i] = old
            else:
                del os.environ[i]

        username_old = os.environ.get('USERNAME')
        password_old = os.environ.get('PASSWORD')
        os.environ.update({
            'USERNAME': 'username_test',
            'PASSWORD': 'password_test'
        }
        )
        self.assertEqual(MtSignClass().username, 'username_test')
        self.assertEqual(MtSignClass().password, 'password_test')
        if username_old:
            os.environ['USERNAME'] = username_old
        else:
            del os.environ['USERNAME']
        if password_old:
            os.environ['PASSWORD'] = password_old
        else:
            del os.environ['PASSWORD']

    def __get_hash(self):
        mt = MtSignClass()
        value = mt._MtSignClass__get_hash()
        self.assertIsInstance(value, (type(None), tuple))
        if value:
            for i in value:
                self.assertIsInstance(i, str)
        return mt, value

    def __login(self, mt, value):
        status = mt._MtSignClass__login(*value)
        self.assertIsInstance(status, bool)
        return status

    def __sign_in(self, mt):
        status = mt._MtSignClass__sign_in()
        self.assertIsInstance(status, bool)
        return status

    def test_run(self):
        mt, value = self.__get_hash()
        self.assertIsNot(value, None)
        self.assertTrue(self.__login(mt, value))
        self.assertTrue(self.__sign_in(mt))

    def test_sign_page(self):
        mt = MtSignClass()
        html = mt.sign_page()
        _hash = mt.sign_page('hash')
        self.assertIsInstance(html, str)
        self.assertIsInstance(_hash, str)
        self.assertNotEqual(html, _hash)
