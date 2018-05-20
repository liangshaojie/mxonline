# coding=utf-8
import json
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile,EmailVerifyRecord
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetPwForm,ResetForm,UploadImageForm,UpdatePwdForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.send_email import send
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
from operation.models import UserCourse,UserFavorite
from organization.models import CourseOrg

class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class LoginView(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", )
                else:
                    return render(request, "login.html", {"msg": "没有激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误"})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"register_form":register_form,"msg": "用户已存在"})
            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            encrypt_pw = make_password(pass_word)
            user_profile.password = encrypt_pw
            user_profile.save()

            send(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{"register_form":register_form})

class ActiveUserView(View):
    def get(self, request, active_code):
        records = EmailVerifyRecord.objects.filter(code=active_code)
        if records:
            for record in records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')

class ForgetPwView(View):
    def get(self, request):
        forgetpw_form = ForgetPwForm()
        return render(request, 'forgetpwd.html',{'forgetpw_form': forgetpw_form})

    def post(self, request):
        forgetpw_form = ForgetPwForm(request.POST)
        if forgetpw_form.is_valid():
            email = request.POST.get('email', '')
            # 这个邮箱是否注册了?
            records = UserProfile.objects.filter(email=email)
            if records:
                for record in records:
                    send(record.email, 'forget')
                return render(request, 'send_sucess.html')
            else:
                return render(request, 'forgetpwd.html', {'msg': '无效的邮箱'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpw_form': forgetpw_form})

class ResetPwView(View):
    def get(self, request, forget_code):
        try:
            record = EmailVerifyRecord.objects.get(code=forget_code)
            email = record.email
            return render(request, 'password_reset.html', {
                'email': email
            })

        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return render(request, 'reset_fail.html')

class ModifyPwView(View):
    def post(self, request):
        resetform = ResetForm(request.POST)
        if resetform.is_valid():
            pw = request.POST.get('password', '')
            pw2 = request.POST.get('password2', '')
            if pw == pw2:
                email = request.POST.get('email', '')
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pw2)
                user.save()
                return render(request, 'login.html', {})
            else:
                return render(request, 'password_reset.html', {'msg': '两次输入的密码不相同'})
        else:
            return render(request, 'password_reset.html', {
                'reset_form': resetform
            })

class UserInfoView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UpdateImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    # 修改密码
    def post(self, request):
        resetform = UpdatePwdForm(request.POST)
        if resetform.is_valid():
            pw = request.POST.get('password1', '')
            pw2 = request.POST.get('password2', '')
            if pw == pw2:
                user = request.user
                user.password = make_password(pw2)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(resetform.errors), content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send(email,'updateEmail')
        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateEmailView(LoginRequiredMixin,View):
    # 修改个人邮箱
    def post(self,request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="updateEmail")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

class MyCourseView(LoginRequiredMixin,View):
    # 我的课程
    def get(self,request):
        user_courses = UserCourse.objects.filter(user = request.user)
        return render(request,"usercenter-mycourse.html",{
            "user_courses":user_courses
        })

class MyFavOrgView(LoginRequiredMixin,View):
    # 我的课程
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user = request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,"usercenter-fav-org.html",{
            "org_list":org_list
        })







