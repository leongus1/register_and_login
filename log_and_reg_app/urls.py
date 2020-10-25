from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('register/success/', views.login),
    path('logged_out/', views.logout),
    path('check_log/', views.log_check),
]