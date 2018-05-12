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

class CourseOrg(models.Model):
    name = models.CharField(verbose_name=u"机构名称", max_length=50)
    desc = models.TextField(verbose_name=u"机构描述")
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏数", default=0)
    mage = models.ImageField(verbose_name=u"机构图", upload_to='org/%Y/%m', max_length=200)
    address = models.CharField(verbose_name=u"机构地址", max_length=150)
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", )
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    name = models.CharField(verbose_name=u"教师名", max_length=50)
    work_years = models.IntegerField(verbose_name=u"工作年限", default=0)
    work_company = models.CharField(verbose_name=u"就职公司", max_length=50)
    work_position = models.CharField(verbose_name=u"工作职位", max_length=50)
    points = models.CharField(verbose_name="u教学特点", max_length=50)
    click_nums = models.IntegerField(verbose_name=u"点击数", default=0)
    fav_nums = models.IntegerField(verbose_name=u"收藏数", default=0)
    add_time = models.DateTimeField(verbose_name=u"添加时间", default=datetime.now)
    organization = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    # avatar = models.ImageField(verbose_name="头像", upload_to='org/teacher/111', max_length=200, default='')
    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name
