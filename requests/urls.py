from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_service_request, name='create_request'),
    path('<int:request_id>/', views.request_detail, name='request_detail'),
    path('all/', views.all_requests, name='all_requests'),
] 