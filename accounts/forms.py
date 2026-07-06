from django import forms
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Role, User
from volunteers.models import Person

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

class UserRegistrationForm(forms.Form):
    forename = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    emergency_contact = forms.CharField(max_length=200)
    notification_preference = forms.ChoiceField(choices=Person.NOTIFICATION_PREFERENCE_CHOICES)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self):
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
            role=self.cleaned_data['role'],
        )

class UserStatusForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role', 'user_status']
