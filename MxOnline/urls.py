# coding=utf-8
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwView,ResetPwView,ModifyPwView,LogoutView,IndexView
from organization.views import OrgView
from django.views.static import serve
from django.conf import settings
urlpatterns = [
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',IndexView.as_view(),name="index"),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)$', ActiveUserView.as_view(), name='active_user'),
    url(r'^forget/$', ForgetPwView.as_view(), name='forget_pwd'),
    url(r'^forgetpw/(?P<forget_code>.*)$', ResetPwView.as_view(), name='reset_pw'),
    url(r'^modifypw/$', ModifyPwView.as_view(), name='modify_pw'),
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^operation/', include('operation.urls', namespace='operation')),
    url(r'^course/', include('courses.urls', namespace='course')),
    url(r'^users/', include('users.urls', namespace='users')),
]
# 全局配置404页面
handler404 = "users.views.page_not_find"
handler500 = "users.views.page_error"
