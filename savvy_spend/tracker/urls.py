from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout', auth_views.LogoutView.as_view()),
    path('register', views.register),
    path('categories/', views.list_categories, name='list_categories'),
    path('add_category/', views.add_category, name='add_category'),
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.list_transactions, name='list_transactions'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('edit_transaction/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('category_transactions/<int:category_id>/', views.category_transactions, name='category_transactions'),
    path('budget/', views.budget, name='budget'),
    path('savings/', views.savings, name='savings'),
    path('savings/add/<int:goal_id>/', views.add_to_savings, name='add_to_savings'),
    path('convert/', views.convert_currency, name='convert_currency'),
    path('savings_forecast/', views.savings_forecast, name='savings_forecast'),
    path('generate_financial_advice/', views.generate_financial_advice, name='generate_financial_advice'),
]
