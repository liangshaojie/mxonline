# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime
from organization.models import CourseOrg

from django.db import models

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,null=True,verbose_name=u"课程机构")
    name = models.CharField(max_length=50,verbose_name=u"课程名")
    desc = models.CharField(max_length=300,verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj","初级"),("zj","中级"),("gz","高级")),max_length=2,verbose_name=u"难度")
    learn_time = models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums = models.IntegerField(verbose_name=u"收藏人数", default=0)
    image = models.ImageField(verbose_name=u"封面图", upload_to='courses/%Y/%m', max_length=100)
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)
    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"章节名", max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节名")
    name = models.CharField(verbose_name=u"视频名", max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"资源名", max_length=100)
    download = models.FileField(verbose_name=u"资源地址", upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
