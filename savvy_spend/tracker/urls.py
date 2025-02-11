from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('login', auth_views.LoginView.as_view()),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout', auth_views.LogoutView.as_view()),
    path('register', views.register),
    path('categories/', views.list_categories, name='list_categories'),
    path('transactions/', views.list_transactions, name='list_transactions')
]
