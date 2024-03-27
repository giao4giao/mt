#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import unittest

from main import main





class TestMain(unittest.TestCase):
    """主方法的测试类测试类"""

    def check_env():
        for i in ['USERNAME', 'PASSWORD']:
            if not os.environ.get(i):
                return True, f"缺少环境变量({i})"
        return False, 'None'

    @unittest.skipIf(*check_env())
    def test_main(self):
        """测试主方法"""
        self.assertEqual(main(),True)

    check_env = staticmethod(check_env)







