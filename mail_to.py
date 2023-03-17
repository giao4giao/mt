# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os


def check(func):
    def wrapper(*args, **kwargs):
        for i in ['mail_pass', 'sender', 'receivers']:
            if not getattr(args[0], i):
                print(f'请先设置环境变量 {i.upper()}')
                return False
                # exit(-1)
        return func(*args, **kwargs)
    return wrapper


class Mail:
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.qq.com"  # 设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass = os.environ.get("MAIL_PASS")  # 刚才我们获取的授权码
        self.sender = os.environ.get("SENDER")  # 你的邮箱地址
        self.receivers = os.environ.get("RECEIVERS")  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    @check
    def send(self,content=''):
        '''你要发送的邮件内容'''
        message = MIMEText(content, 'html', 'utf-8')

        message['From'] = Header("自动签到提醒", 'utf-8')
        message['To'] = Header("你", 'utf-8')

        subject = 'mt论坛自动签到提醒'  # 发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)
            smtpObj.login(self.sender, self.mail_pass)
            smtpObj.sendmail(self.sender, [self.receivers], message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
            return True
        except smtplib.SMTPException as e:
            print('邮件发送失败')
            return False


if __name__ == '__main__':
    mail = Mail()
    mail.send()