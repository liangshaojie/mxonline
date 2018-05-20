# _*_ coding: utf-8 _*_
__author__ = 'daiyaquan'
__date__ = '2018/3/12 5:35'

import random

from django.core.mail import send_mail
from django.conf import settings

from users.models import EmailVerifyRecord


def generate_ranstr(str_len=10):
    chars = 'zxcvbnm12345ASDFGHJKL67890qwertyuiopQWEZXCRTYVBNMUIOP'
    ran = [chars[random.randint(0, str_len - 1)] for _ in range(str_len)]
    return ''.join(ran)


def send(email, send_type="register"):
    # 将这条记录存入数据库
    email_verify = EmailVerifyRecord()
    code = generate_ranstr(16)
    email_verify.code = code
    email_verify.email = email
    email_verify.send_type = send_type
    email_verify.save()

    if send_type == "register":
        email_title = "DEdu在线教育平台 注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        # 如果发送成功
        if send_status:
            pass

    if send_type == 'forget':
        email_title = "DEdu在线教育平台 注册激活链接"
        email_body = "请点击下面的链接进行验证: http://127.0.0.1:8000/forgetpw/{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == 'updateEmail':
        email_title = "DEdu在线教育平台 邮箱修改验证码"
        email_body = "您的邮箱验证码为{0}".format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass
