from django.contrib import admin

from impact.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'report_name', 'programme', 'report_date', 'satisfaction_score')
    list_filter = ('programme',)
