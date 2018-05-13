# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 数据库操作
        orgs = CourseOrg.objects.all()
        cities = CityDict.objects.all()

        # 获取param
        city_id = int(request.GET.get('city', 0))

        # 改变queryset
        if city_id:
            orgs = orgs.filter(city_id=city_id)

        category = request.GET.get('ct', "")
        if category:
            orgs = orgs.filter(category=category)

        # 获取count of queryset
        orgs_count = orgs.count()

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, per_page=3, request=request)

        p_orgs = p.page(page)

        return render(request, 'org-list.html', {
            'p_orgs': p_orgs,
            'cities': cities,
            'orgs_count': orgs_count,
            'city_id': city_id,
            'category':category
        })
