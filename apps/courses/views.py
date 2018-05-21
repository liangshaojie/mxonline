# coding=utf-8
from django.shortcuts import render
from django.views.generic.base import View
from .models import Course,CourseResource,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite,CourseComments,UserCourse
from django.shortcuts import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q

class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords',"")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

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


class CourseDetailView(View):
    def get(self, request,course_id):
        course = Course.objects.get(id = course_id)
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user = request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True


        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []
        return render(request,"course-detail.html",{
            "course":course,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org
        })

class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        all_resources = CourseResource.objects.filter(course=course)

        # 用户搜集用户学了那些课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user,course=course)
            user_courses.save()

        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]

        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_course]

        return render(request, "course-video.html", {
            "course": course,
            "all_resources":all_resources
        })

class CommentsView(LoginRequiredMixin,View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)

        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]

        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_course]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_comment = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comment":all_comment,
            "relate_courses":relate_courses
        })

class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments","")

        if int(course_id) > 0 and comments:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):

        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        all_resources = CourseResource.objects.filter(course=course)

        # 用户搜集用户学了那些课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user,course=course)
            user_courses.save()

        user_course = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_course]

        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_course]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_comment = CourseComments.objects.all()
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comment": all_comment,
            "relate_courses": relate_courses,
            "video":video
        })
