from django.contrib import admin
from django.urls import path
from .views import Mpesa,confirmation,PaymentView,StripeWebhookView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.confirmation, name="confirm"),
    path('pay/', Mpesa.as_view(), name='deposit'),
    path('process-payment/', views.StripeWebhookView, name='processpayment'),
    path('stripe-card-donation/', PaymentView.as_view(), name='stripe-pay'),

]
