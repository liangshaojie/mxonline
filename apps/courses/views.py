from django.shortcuts import render
from django.views.generic.base import View
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]



        sorted = request.GET.get('sort', "")
        if sorted:
            if sorted == "students":
                all_courses = all_courses.order_by("-students")
            elif sorted == "hot":
                all_courses = all_courses.order_by("-click_nums")


        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3, request=request)
        courses = p.page(page)
        return render(request,'course-list.html',{
            "all_courses":courses,
            "sort":sorted,
            "hot_courses":hot_courses
        })