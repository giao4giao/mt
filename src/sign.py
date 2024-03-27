#!/usr/bin/env python
# encoding: utf-8
import os
import re
import sys
from typing import Optional, Tuple
from urllib import parse

import requests

if sys.version_info < (3, 8):
    os.system('pip install typing_extensions')
    from typing_extensions import Literal
else:
    from typing import Literal

METHOD_TYPE = Literal['html', 'hash']


class MtSignClass:
    """签到类"""
    login_url = 'https://bbs.binmt.cc/member.php'
    sign_url = 'https://bbs.binmt.cc/k_misign-sign.html'

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """初始化

        :param username: 用户名
        :param password: 密码
        """
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        self.session = requests.Session()
        self.username = username if username else os.environ.get("USERNAME")
        self.password = password if password else os.environ.get("PASSWORD")
        if not self.username or not self.password:
            raise ValueError("请设置环境变量 USERNAME 和 PASSWORD")

    def __get_hash(self) -> Optional[Tuple[str, str]]:
        """获取登陆所需login_hash和form_hash

        :return: 登录哈希和表单哈希
        """
        params = {
            "mod": "logging",
            "action": "login",
            "infloat": "yes",
            "handlekey": "login",
            "inajax": 1,
            "ajaxtarget": "fwin_content_login"
        }
        self.headers['referer'] = f"{self.login_url}?{parse.urlencode(params)}"
        res = self.session.get(url=self.login_url, params=params, headers=self.headers)
        if res.ok:
            page_text = res.text
            login_hash = re.findall('loginhash=(.*?)">', page_text, re.S)[0]
            form_hash = re.findall('formhash" value="(.*?)".*? />', page_text, re.S)[0]
            return login_hash, form_hash
        return None  # pragma: no cover

    def __login(self, login_hash: str, form_hash: str) -> bool:
        """模拟登陆

        :param login_hash:登录哈希
        :param form_hash: 表单哈希
        :return: 登录是否成功
        """
        params = {
            "mod": "logging",
            "action": "login",
            "loginsubmit": "yes",
            "handlekey": "login",
            "loginhash": login_hash,
            "inajax": "1"
        }
        data = {
            'formhash': form_hash,
            'referer': 'https://bbs.binmt.cc/index.php',
            'loginfield': 'username',
            'username': self.username,
            'password': self.password,
            'questionid': '0',
            'answer': '',  # TODO 这里看上去是回答问题登录（暂不支持）
        }
        res = self.session.post(url=self.login_url, params=params, headers=self.headers, data=data)
        # print(res.text)
        # 验证是否登陆成功
        check = re.match('.*?<root>(.*?)</root>', res.text, re.S)
        if check:
            # TODO 这里的需要改一下，下次再改吧
            check2 = re.search('(?P<msg>登录失败，您还可以尝试\s?(?P<num>\d+)\s?次)', res.text)
            if check2:
                print(check2.group('msg'))
                return False
            check3 = re.search('(?P<msg>请输入验证码后继续登录)', res.text)
            if check3:  # TODO 这里多次登录失败需要输入验证码（没有处理）
                print(check3.group('msg'))
                return False
            if re.search('欢迎您回来', res.text):
                return True
        match = re.search("[a-z]\('(?P<msg>.*?)',\s*?\{.*?\}\)", res.text)
        if match:
            print(match.group('msg'))
        return False  # pragma: no cover

    def sign_page(self, method: METHOD_TYPE = 'html') -> str:
        """获取签到所需的form_hash或者签到界面hmtl源码

        :param method: 选择模式
        :return: form_hash值或签到界面
        """
        self.headers['referer'] = self.sign_url
        res = self.session.get(url=self.sign_url, headers=self.headers)
        if res.ok:
            if method == 'hash':
                form_hash = re.findall('formhash" value="(.*?)".*? />', res.text, re.S)
                if form_hash:
                    return form_hash[0]
                raise ValueError('获取签到所需的hash值失败')  # pragma: no cover
            elif method == 'html':
                html = res.text
                if re.search('<a .*?>(?P<value>登录)</a>', html):  # 判断是否登录，如果没有登录就进行登录
                    if self.__login(*self.__get_hash()):
                        print('登录成功')
                        return self.sign_page()
                return html
            raise ValueError(f'输入了不支持的method参数({method})')  # pragma: no cover

    def __sign_in(self) -> bool:
        """模拟签到

        :return: 签到是否成功
        """
        form_hash = self.sign_page('hash')
        if form_hash:
            # 模拟签到
            sign_url = 'https://bbs.binmt.cc/plugin.php'
            params = {
                "id": "k_misign:sign",
                "operation": "qiandao",
                "format": "text",
                "formhash": form_hash
            }
            self.headers['referer'] = f"{self.sign_url}?{parse.urlencode(params)}"
            res = self.session.get(url=sign_url, params=params, headers=self.headers)
            if res.ok:
                # 验证是否签到成功
                check = re.search(r'<root>(?P<notice>.*?)</root>', res.text, re.S)
                if check:
                    # print('签到成功')
                    value = re.search(r'[A-Z]\[(?P<notice>.*?)\]', check.group('notice'))
                    print(value.group('notice'))
                    return True
            print('签到失败')  # pragma: no cover
            return False  # pragma: no cover
        raise ValueError('签到状态码错误')  # pragma: no cover

    def run(self) -> Optional[bool]:
        """一键签到

        :return: 签到是否成功
        """
        hash_value = self.__get_hash()
        if hash_value:
            if self.__login(*hash_value):
                print('登录成功')
                return self.__sign_in()
        else:
            raise ValueError('获取登录所需的hash值失败')  # pragma: no cover

    def __del__(self):
        self.session.close()


if __name__ == '__main__':
    mt = MtSignClass()  # pragma: no cover
    mt.run()  # pragma: no cover
