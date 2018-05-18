# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime
from organization.models import CourseOrg,Teacher

from django.db import models

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg,null=True,verbose_name=u"课程机构")
    name = models.CharField(max_length=50,verbose_name=u"课程名")
    desc = models.CharField(max_length=300,verbose_name=u"课程描述")
    teacher = models.ForeignKey(Teacher,null=True, verbose_name=u"讲师")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj","初级"),("zj","中级"),("gz","高级")),max_length=2,verbose_name=u"难度")
    learn_time = models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums = models.IntegerField(verbose_name=u"收藏人数", default=0)
    image = models.ImageField(verbose_name=u"封面图", upload_to='courses/%Y/%m', max_length=100)
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    category = models.CharField(verbose_name=u"课程类别",max_length=20,default="后端开发")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(max_length=300,default="",verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=200,default="",verbose_name=u"老师告诉你")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)
    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    # 获取课程所有章节
    def get_learn_lesson(self):
        return self.lesson_set.all()

    # 获取章节数量
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"章节名", max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    # 获取章节视频
    def get_learn_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节名")
    name = models.CharField(verbose_name=u"视频名", max_length=100)
    url = models.CharField(verbose_name=u"访问地址",default="", max_length=200)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长（分钟）")
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(verbose_name=u"资源名", max_length=100)
    download = models.FileField(verbose_name=u"资源地址", upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name


    def __unicode__(self):
        return self.name
