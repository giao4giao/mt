#!/usr/bin/env python
# encoding: utf-8
import os
import unittest

from src.parse import ParseMtClass


class TestParse(unittest.TestCase):
    def test_init(self):
        parse = ParseMtClass('username_test', 'password_test')
        self.assertEqual(parse.username, 'username_test')
        self.assertEqual(parse.password, 'password_test')

        for i in ('USERNAME', 'PASSWORD'):
            old = os.environ.get(i)
            os.environ[i] = ''
            with self.assertRaises(ValueError):
                ParseMtClass()
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
        self.assertEqual(ParseMtClass().username, 'username_test')
        self.assertEqual(ParseMtClass().password, 'password_test')
        if username_old:
            os.environ['USERNAME'] = username_old
        else:
            del os.environ['USERNAME']
        if password_old:
            os.environ['PASSWORD'] = password_old
        else:
            del os.environ['PASSWORD']

    def test_now_time(self):
        self.assertIsInstance(ParseMtClass.now_time(), str)

    def test_read_to_html(self):
        parse = ParseMtClass()
        self.assertIsInstance(parse.read_to_html(), str)

    def test_get_more_data(self):
        with open('html/sign.html', 'r', encoding='utf8') as f:
            html = f.read().replace('  ', '').replace('\n', ' ')
        parse = ParseMtClass()
        dct = parse._get_more_data(html)
        self.assertIsInstance(dct, dict)
        self.assertEqual(len(dct), 6)

    def test_parse_more_data(self):
        with open('html/sign.html', 'r', encoding='utf8') as f:
            html = f.read().replace('  ', '').replace('\n', ' ')
        parse = ParseMtClass()
        dct = parse._parse_more_data(html)
        self.assertIsInstance(dct, dict)
        self.assertEqual(len(dct), 6)

    def test_read_to_html(self):
        parse = ParseMtClass()
        dct = {
            'continue': '1', 'class': 'LV.1', 'award': '1',
            'all_day': '100', 'num': '1000',
            'name': '你的用户名'
        }
        html = parse.read_to_html(dct)
        html_None = parse.read_to_html({})
        self.assertIsInstance(html, str)
        self.assertIsInstance(html_None, str)
        self.assertNotEqual(html_None, html)

    def test_get_num(self):
        lst = [
            '<span class="one"></span>',
            '<span class="one"></span>',
            '<span class="one"></span>',
            '<span class="one"></span><span class="zero"></span><span class="zero"></span>'
        ]
        parse = ParseMtClass()
        for i in range(len(lst)):
            self.assertIsInstance(parse._ParseMtClass__get_num(lst, i), str)
