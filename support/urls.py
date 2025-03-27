from django.urls import path
from . import views

urlpatterns = [
    path('', views.support_login, name='support_login'),
    path('dashboard/', views.support_dashboard, name='support_dashboard'),
    path('register/', views.register_support, name='register_support'),
    path('setup/<str:token>/', views.setup_support_user, name='setup_support_user'),
] 