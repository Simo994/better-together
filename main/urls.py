from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('create-request/', views.create_request, name='create_request'),
    path('delete-request/<int:pk>/', views.delete_request, name='delete_request'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('update-request-status/<int:pk>/', views.update_request_status, name='update_request_status'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('api/solved-count/', views.get_solved_count, name='get_solved_count'),
]
