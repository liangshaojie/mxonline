
from django import forms

class UserAskForm(forms):
    name = forms.CharField(required=True,min_length=2,max_length=20)