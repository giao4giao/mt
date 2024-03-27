#!/usr/bin/env python
# encoding: utf-8
import os

from src import *


def main():
    print("当前时间:", ParseMtClass.now_time())
    mt = ParseMtClass()
    mt.run()
    if os.environ.get("SEND"):  # 是否发送邮件，默认是不发送
        html_text = mt.read_to_html()
        m = Mail()
        m.send(html_text)
    return True


if __name__ == '__main__':
    main() # pragma: no cover
