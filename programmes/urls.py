from django.urls import path

from programmes import views

app_name = 'programmes'

urlpatterns = [
    path('', views.programme_list, name='programme_list'),
    path('new/', views.programme_create, name='programme_create'),
    path('<int:programme_id>/', views.programme_detail, name='programme_detail'),
    path('<int:programme_id>/edit/', views.programme_edit, name='programme_edit'),
    path('<int:programme_id>/events/new/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/assign/', views.assignment_add, name='assignment_add'),
    path('assignments/<int:assignment_id>/attendance/', views.assignment_attendance_toggle, name='assignment_attendance_toggle'),
    path('assignments/<int:assignment_id>/remove/', views.assignment_remove, name='assignment_remove'),
]
