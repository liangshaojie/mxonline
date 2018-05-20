# -*- coding:utf-8 -*-
__author__ = "lsj"
__date__ = '2018/5/12/012 21:45'

from django import forms

from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


class ForgetPwForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class ResetForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=4)
    password2 = forms.CharField(required=True, min_length=4)

class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=4)
    password2 = forms.CharField(required=True, min_length=4)

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']