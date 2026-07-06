from django import forms

from impact.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['programme', 'report_name', 'report_date', 'satisfaction_score']
        widgets = {'report_date': forms.DateInput(attrs={'type': 'date'})}
