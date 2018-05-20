# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    GENDER_CHOICE = (
        ('male', u'男'),
        ('female', u'女'),
    )
    nick_name = models.CharField(verbose_name=u"昵称", max_length=20, default='')
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(verbose_name=u"性别", choices=GENDER_CHOICE, default='male', max_length=8)
    address = models.CharField(verbose_name=u"地址", max_length=200, default='')
    mobile = models.CharField(verbose_name=u"手机号", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name=u"头像", upload_to="image/user/profile/", default='image/user/default.png',
                              max_length=200)
    def unread_nums(self):
        # 获取用户未读消息数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id).count()


    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    SEND_CHOICE = (
        ('register', u'注册账号'),
        ('forget', u'找回密码'),
        ('updateEmail',u'修改邮箱')
    )
    code = models.CharField(verbose_name=u"验证码",null=True, max_length=20)
    email = models.EmailField(verbose_name=u"邮箱", max_length=50)
    send_type = models.CharField(verbose_name=u"类型", choices=SEND_CHOICE, max_length=20)
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0} {1}'.format(self.code,self.email)

class Banner(models.Model):
    title = models.CharField(verbose_name=u"标题", max_length=100, default='')
    image = models.ImageField(verbose_name=u"播放图片", upload_to='banner/%Y/%m/', max_length=200)
    index = models.IntegerField(verbose_name=u"播放顺序", default=100)
    url = models.CharField(verbose_name=u"访问地址", max_length=200)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.index

