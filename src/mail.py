#!/usr/bin/env python
# encoding: utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from functools import wraps


class Mail:
    def __init__(self, mail_username=None, mail_password=None, receivers=None, mail_host="smtp.qq.com", port=465):
        """初始化 第三方 SMTP 服务"""
        self.mail_host = os.environ.get("MAIL_HOST") if os.environ.get("MAIL_HOST") else mail_host  # 设置服务器
        self.mail_pass = mail_password if mail_password else os.environ.get("MAIL_PASS")  # 邮箱登录授权码
        self.sender = mail_username if mail_username else os.environ.get("SENDER")  # 自己的邮箱地址
        self.receivers = receivers if receivers else os.environ.get("RECEIVERS")  # 收件人的邮箱地址，不可多个
        self.port = int(os.environ.get("MAIL_PORT")) if int(os.environ.get("MAIL_PORT")) else port  # 服务器端口

    def check(func):
        """检测环境的装饰器"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in ['mail_pass', 'sender', 'receivers']:
                if not getattr(args[0], i):
                    print(f'请先设置环境变量 {i.upper()}')
                    return False
            return func(*args, **kwargs)

        return wrapper

    @check
    def send(self, content='default', subject='mt论坛自动签到提醒'):
        """你要发送的邮件内容

        :param content: 发送的内容
        :param subject: 发送的主题
        :return:
        """
        message = MIMEText(content, 'html', 'utf-8')

        message['From'] = Header("自动签到提醒", 'utf-8')
        message['To'] = Header("你", 'utf-8')

        message['Subject'] = Header(subject, 'utf-8')
        smtpObj = None
        try:
            if self.port == 587:
                smtpObj = smtplib.SMTP(self.mail_host, 587)
                smtpObj.starttls()  # 启动安全连接
            else:
                smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, [self.receivers], message.as_string())
            print('邮件发送成功')
            return True
        except smtplib.SMTPException as e:
            print('邮件发送失败')
            return False
        finally:
            if smtpObj:
                smtpObj.quit()

    check = staticmethod(check)


if __name__ == '__main__':
    mail = Mail()  # pragma: no cover
    mail.send()  # pragma: no cover
