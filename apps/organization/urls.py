# -*- coding:utf-8 -*-
__author__ = "lsj"
__date__ = '2018/5/13/013 20:20'
from django.conf.urls import url
from .views import OrgView

urlpatterns = [
    url(r'list/$', OrgView.as_view(), name='list'),
    # url(r'home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    # url(r'course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='course'),
    # url(r'desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='desc'),
    # url(r'teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='teacher'),
]