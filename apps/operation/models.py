# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

class UserAsk(models.Model):
    name = models.CharField(verbose_name=u"姓名", max_length=20)
    mobile = models.CharField(verbose_name=u"手机", max_length=11)
    course_name = models.CharField(verbose_name=u"课程名", max_length=50)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'用户询问'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    comments = models.CharField(verbose_name=u"评论", max_length=200)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    TYPE_CHOICE = (
        ('1', '课程'),
        ('2', '课程机构'),
        ('3', '讲师')
    )
    user = models.ForeignKey(to=UserProfile, verbose_name=u"用户")
    fav_id = models.IntegerField(verbose_name=u"收藏对应的id名", default=0)
    fav_type = models.CharField(verbose_name=u"收藏类型", default=1, max_length=1, choices=TYPE_CHOICE)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(verbose_name=u"接受用户", default=0)
    message = models.CharField(verbose_name=u"消息", max_length=500)
    has_read = models.BooleanField(verbose_name=u"是否读过", default=False)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'用户课程表'
        verbose_name_plural = verbose_name



