# coding=utf-8
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic.base import View
from courses.models import Course, CourseOrg, Teacher

from .models import UserFavorite


class ChangeFavView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        else:
            fav_id = int(request.POST.get('fav_id', 0))
            fav_type = int(request.POST.get('fav_type', 0))
            try:
                user_fav = UserFavorite.objects.get(user=request.user, fav_id=fav_id, fav_type=fav_type)
                user_fav.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums -= 1
                    if course_org.fav_nums < 0:
                        course_org.fav_nums = 0
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
            except ObjectDoesNotExist:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
