from django import forms

from accounts.models import Role, User
from programmes.models import Event, Programme, VolunteerAssignment


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ['programme_name', 'programme_description', 'location', 'start_date', 'end_date', 'status', 'programme_cost']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'programme_description': forms.Textarea(attrs={'rows': 3}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_description', 'start_date', 'end_date', 'status', 'capacity', 'required_skills']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'event_description': forms.Textarea(attrs={'rows': 3}),
            'required_skills': forms.CheckboxSelectMultiple,
        }


class VolunteerAssignmentForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role__role_name=Role.VOLUNTEER).select_related('person'),
        label='Volunteer',
    )

    class Meta:
        model = VolunteerAssignment
        fields = ['user', 'volunteer_role']
