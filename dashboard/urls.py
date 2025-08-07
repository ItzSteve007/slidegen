from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_images, name='upload_images'),
    path('create-ppt/', views.create_ppt, name='create_ppt'),
]
