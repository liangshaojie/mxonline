# encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    GENDER_CHOICE = (
        ('male', u'男'),
        ('female', u'女'),
    )
    nick_name = models.CharField(verbose_name=u"昵称", max_length=20, default='')
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", choices=GENDER_CHOICE, default='male', max_length=6)
    address = models.CharField(verbose_name=u"地址", max_length=200, default='')
    mobile = models.CharField(verbose_name=u"手机号", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u"头像", upload_to="image/user/profile/", default='image/user/default.png',
                              max_length=200)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.username
