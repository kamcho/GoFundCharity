from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Q_A/', QandA.as_view(), name='quizes'),
    path('', Home.as_view(), name='home'),
    path('About/', Contacts.as_view(), name='info'),
]