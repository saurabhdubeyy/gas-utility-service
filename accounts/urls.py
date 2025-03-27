from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_dashboard, name='customer_dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
] 