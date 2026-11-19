from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('transfer/', views.money_transfer, name='transfer'),
    path('statement/', views.account_statement, name='statement'),
    path('pay-bills/', views.pay_bills, name='pay_bills'),
    path('bill-history/', views.bill_history, name='bill_history'),
    path('complaint/', views.raise_complaint, name='complaint'),
    path('complaint-history/', views.complaint_history, name='complaint_history'),
    path('profile/', views.profile, name='profile'),
]