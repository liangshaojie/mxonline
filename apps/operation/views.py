# coding=utf-8
from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic.base import View

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
                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
            except ObjectDoesNotExist:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')