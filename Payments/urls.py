from django.contrib import admin
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('confirmation/', views.confirmation, name="confirmation"),
    path('pay/', Mpesa.as_view(), name='deposit'),

]
