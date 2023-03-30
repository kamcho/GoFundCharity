from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser,Project

class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password1', 'password2')

class StartProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=('first_name','last_name','target_country','target_city','target_area','title')

class StartProjectForm2(forms.ModelForm):

    class Meta:
        model=Project
        fields=('target_relationship','problem','solution','target_amount','expiry')