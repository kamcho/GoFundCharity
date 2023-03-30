from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register',views.register, name='register'),
    path('',Home.as_view(),name='home'),
    path('go-fund/',StartCharity.as_view(),name='gofund'),
    path('confirm-details/', ConfirmProject.as_view(), name='confirmproject'),

    path('profile/',Profiles.as_view(),name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
]