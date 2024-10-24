from django.urls import path
from django.shortcuts import render, redirect
from . import views

app_name = 'loginRegister'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.ViewsLogout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate')
]