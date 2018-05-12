# -*- coding:utf-8 -*-
__author__ = "lsj"
__date__ = '2018/5/12/012 16:30'

import xadmin

from .models import CityDict, CourseOrg, Teacher


# 机构所属城市名后台管理器
class CityDictAdmin(object):
    list_display = ['name', 'desc','add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc','add_time']


# 机构课程信息管理器
class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'address', 'add_time']


class TeacherAdmin(object):


    list_display = ['name', 'work_years', 'work_company', 'work_position','points','click_nums','fav_nums','add_time','organization']
    search_fields =['name', 'work_years', 'work_company', 'work_position','points','click_nums','fav_nums','organization']
    list_filter = ['name', 'work_years', 'work_company', 'work_position','points','click_nums','fav_nums','add_time','organization']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
