from django.urls import path

from volunteers import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.volunteer_list, name='volunteer_list'),
    path('register/', views.volunteer_register, name='volunteer_register'),
    path('skills/', views.skill_list, name='skill_list'),
    path('<int:user_id>/', views.volunteer_detail, name='volunteer_detail'),
    path('<int:user_id>/edit/', views.person_edit, name='person_edit'),
    path('<int:user_id>/dbs/add/', views.dbs_status_add, name='dbs_status_add'),
    path('<int:user_id>/availability/add/', views.availability_add, name='availability_add'),
    path('availability/<int:availability_id>/delete/', views.availability_delete, name='availability_delete'),
    path('<int:user_id>/skills/add/', views.volunteer_skill_add, name='volunteer_skill_add'),
    path('skills/<int:volunteer_skill_id>/delete/', views.volunteer_skill_delete, name='volunteer_skill_delete'),
]
