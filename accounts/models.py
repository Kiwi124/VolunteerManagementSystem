from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from volunteers.models import Person

class Role(models.Model):
    ADMIN = 'Administrator'
    PROGRAMME_COORDINATOR = 'Programme Coordinator'
    OPERATIONS_MANAGER = 'Operations Manager'
    FUNDER_RELATIONS_MANAGER = 'Funder-Relations Manager'
    VOLUNTEER_COORDINATOR = 'Volunteer Coordinator'
    VOLUNTEER = 'Volunteer'

    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name

class UserManager(BaseUserManager):
    def create_user(self, email, password, person, role, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, person=person, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, person, role, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, person, role, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    SUSPENDED = 'SUSPENDED'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (SUSPENDED, 'Suspended'),
    ]

    user_id = models.AutoField(primary_key=True)
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name='user_account',
    )
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    user_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=ACTIVE,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_active(self):
        return self.user_status == self.ACTIVE

    @property
    def is_staff(self):
        return self.is_active and self.role_id is not None and self.role.role_name != Role.VOLUNTEER

    def __str__(self):
        return f'{self.person} <{self.email}>'

class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs',
    )
    action_performed = models.CharField(max_length=50)
    entity_affected = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.timestamp} {self.user} {self.action_performed} {self.entity_affected}'
