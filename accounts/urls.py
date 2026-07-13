from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/new/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('audit-log/', views.audit_log_list, name='audit_log_list'),
    path('backup/', views.trigger_backup, name='trigger_backup'),
]
