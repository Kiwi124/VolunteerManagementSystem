from django import forms

from accounts.models import Role, User
from volunteers.models import Availability, DBSStatus, Person, Skill, VolunteerSkill

class VolunteerRegistrationForm(forms.Form):
    forename = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    emergency_contact = forms.CharField(max_length=200)
    notification_preference = forms.ChoiceField(choices=Person.NOTIFICATION_PREFERENCE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self):
        volunteer_role, _ = Role.objects.get_or_create(role_name=Role.VOLUNTEER)
        person = Person.objects.create(
            forename=self.cleaned_data['forename'],
            surname=self.cleaned_data['surname'],
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data['address'],
            emergency_contact=self.cleaned_data['emergency_contact'],
            notification_preference=self.cleaned_data['notification_preference'],
        )
        return User.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            person=person,
            role=volunteer_role,
        )

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['forename', 'surname', 'phone_number', 'address', 'emergency_contact', 'notification_preference']

class DBSStatusForm(forms.ModelForm):
    class Meta:
        model = DBSStatus
        fields = ['dbs_status', 'dbs_expiry']
        widgets = {'dbs_expiry': forms.DateInput(attrs={'type': 'date'})}

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'skill_description']

class VolunteerSkillForm(forms.ModelForm):
    class Meta:
        model = VolunteerSkill
        fields = ['skill', 'skill_level']
