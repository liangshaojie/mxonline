# -*- coding:utf-8 -*-
__author__ = "lsj"
__date__ = '2018/5/19/019 21:17'

from django.conf.urls import url
from .views import UserInfoView,UpdateImageView,UpdatePwdView


urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    # 用户上传头像
    url(r'^image/upload/$', UpdateImageView.as_view(), name='user_upload'),

    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

]