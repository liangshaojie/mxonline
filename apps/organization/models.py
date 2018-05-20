# encoding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

class CityDict(models.Model):
    name = models.CharField(verbose_name=u"城市名", max_length=20)
    desc = models.CharField(verbose_name=u"描述", max_length=200)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name



class CourseOrg(models.Model):
    ORG_CHOICE = (
        ('pxjg', '培训机构'),
        ('gx', '高校'),
        ('gr', '个人')
    )
    name = models.CharField(verbose_name=u"机构名称", max_length=50)
    desc = models.TextField(verbose_name=u"机构描述")
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏数", default=0)
    category = models.CharField(verbose_name=u"机构类别", max_length=4, choices=ORG_CHOICE, default='pxjg')
    image = models.ImageField(verbose_name=u"机构图", upload_to='org/%Y/%m', max_length=200)
    address = models.CharField(verbose_name=u"机构地址", max_length=150)
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", )
    students = models.IntegerField(verbose_name=u"学习人数", default=0)
    course_nums = models.IntegerField(verbose_name=u"课程数", default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(verbose_name=u"教师名", max_length=50)
    age = models.IntegerField(verbose_name=u"年龄",default=18,)
    work_years = models.IntegerField(verbose_name=u"工作年限", default=0)
    work_company = models.CharField(verbose_name=u"就职公司", max_length=50)
    work_position = models.CharField(verbose_name=u"工作职位", max_length=50)
    points = models.CharField(verbose_name="u教学特点", max_length=50)
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏数", default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)
    organization = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    avatar = models.ImageField(verbose_name="头像", upload_to='teacher/%Y/%m', max_length=200, default='')
    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def __unicode__(self):
        return self.name
