from django.urls import path
from . import views

urlpatterns = [
    path('', views.otp, name='otp'),
    path('verify/', views.verify_otp, name='verify_otp'),
]