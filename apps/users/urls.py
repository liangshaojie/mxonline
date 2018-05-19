# -*- coding:utf-8 -*-
__author__ = "lsj"
__date__ = '2018/5/19/019 21:17'

from django.conf.urls import url
from .views import UserInfoView


urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
]