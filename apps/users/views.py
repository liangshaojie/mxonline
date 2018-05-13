# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile,EmailVerifyRecord
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ForgetPwForm,ResetForm
from django.contrib.auth.hashers import make_password
from utils.send_email import send
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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