# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from .models import CityDict, CourseOrg,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse
from operation.models import UserFavorite


def isFav(request, fav_id):
    is_fav = False
    # 用户登陆, 并且有这条收藏记录
    if request.user.is_authenticated:
        if UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=2):
            is_fav = True
    return is_fav

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 数据库操作
        orgs = CourseOrg.objects.all()
        cities = CityDict.objects.all()
        hot_orgs = orgs.order_by("click_nums")[:3]

        # 获取param
        city_id = int(request.GET.get('city', 0))

        # 改变queryset
        if city_id:
            orgs = orgs.filter(city_id=city_id)

        category = request.GET.get('ct', "")
        if category:
            orgs = orgs.filter(category=category)

        sorted = request.GET.get('sort', "")
        if sorted:
            if sorted == "student":
                orgs = orgs.order_by("students")
            elif sorted == "courses":
                orgs = orgs.order_by("course_nums")

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
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sorted
        })

class AddUserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}',content_type='application/json')

class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=int(org_id))
        courses = org.course_set.all()[:4]
        teacher = org.teacher_set.all()[:1][0]

        return render(request, 'org-detail-homepage.html', {
            'courses': courses,
            'teacher': teacher,
            'org': org,
            'is_fav': isFav(request, org.id),
            'current_page':current_page
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        org = CourseOrg.objects.get(id=int(org_id))
        courses = org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'courses': courses,
            'org': org,
            'is_fav': isFav(request, org.id),
            'current_page': current_page
        })

class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'org': org,
            'is_fav': isFav(request, org.id),
            'current_page': current_page
        })

class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.get(id=int(org_id))
        teachers = org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'teachers': teachers,
            'is_fav': isFav(request, org.id),
            'current_page': current_page
        })

class TeacherListView(View):
    """课程讲师列表页面"""
    def get(self,request):
        all_teachers = Teacher.objects.all()

        sorted = request.GET.get('sort', "")

        if sorted == "hot":
            all_teachers = all_teachers.order_by("-click_nums")

        sorted_teacher = Teacher.objects.all().order_by("-click_nums")[:3]

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=2, request=request)

        all_teachers = p.page(page)

        return render(request,"teachers-list.html",{
            "all_teachers":all_teachers,
            "sorted_teacher":sorted_teacher,
            "sorted":sorted
        })