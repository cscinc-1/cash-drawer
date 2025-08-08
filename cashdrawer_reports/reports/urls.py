from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('daily-transactions/', views.daily_transactions, name='daily_transactions'),
    path('accounts/', views.accounts_report, name='accounts_report'),
]