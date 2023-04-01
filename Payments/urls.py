from django.contrib import admin
from django.urls import path
from .views import Mpesa,confirmation
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.confirmation, name="confirm"),
    path('pay/', Mpesa.as_view(), name='deposit'),

]
