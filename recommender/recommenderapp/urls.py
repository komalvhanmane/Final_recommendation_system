from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
