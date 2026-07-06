from django.urls import path

from impact import views

app_name = 'impact'

urlpatterns = [
    path('dashboard/', views.impact_dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/new/', views.report_create, name='report_create'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
]
