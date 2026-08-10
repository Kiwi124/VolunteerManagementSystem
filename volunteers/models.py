from django.conf import settings
from django.db import models

class Person(models.Model):
    NOTIFY_EMAIL = 'EMAIL'
    NOTIFY_SMS = 'SMS'
    NOTIFY_PHONE = 'PHONE'
    NOTIFY_NONE = 'NONE'
    NOTIFICATION_PREFERENCE_CHOICES = [
        (NOTIFY_EMAIL, 'Email'),
        (NOTIFY_SMS, 'SMS / Text'),
        (NOTIFY_PHONE, 'Phone Call'),
        (NOTIFY_NONE, 'No Reminders'),
    ]

    person_id = models.AutoField(primary_key=True)
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    emergency_contact = models.CharField(max_length=200)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    notification_preference = models.CharField(
        max_length=10,
        choices=NOTIFICATION_PREFERENCE_CHOICES,
        default=NOTIFY_EMAIL,
    )

    def __str__(self):
        return f'{self.forename} {self.surname}'

    @property
    def initials(self):
        forename_initial = (self.forename or '').strip()[:1]
        surname_initial = (self.surname or '').strip()[:1]
        return f'{forename_initial}{surname_initial}'.upper()

class DBSStatus(models.Model):
    NOT_STARTED = 'NOT_STARTED'
    PENDING = 'PENDING'
    CLEARED = 'CLEARED'
    EXPIRED = 'EXPIRED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (NOT_STARTED, 'Not Started'),
        (PENDING, 'Pending'),
        (CLEARED, 'Cleared'),
        (EXPIRED, 'Expired'),
        (REJECTED, 'Rejected'),
    ]

    dbs_status_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='dbs_statuses',
    )
    dbs_status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=NOT_STARTED,
    )
    dbs_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.person} - {self.get_dbs_status_display()}'

class Availability(models.Model):
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    availability_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities',
    )
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.user} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}'

class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100, unique=True)
    skill_description = models.TextField(blank=True)

    def __str__(self):
        return self.skill_name

class VolunteerSkill(models.Model):
    BEGINNER = 'BEGINNER'
    INTERMEDIATE = 'INTERMEDIATE'
    EXPERT = 'EXPERT'
    SKILL_LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (EXPERT, 'Expert'),
    ]

    volunteer_skill_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_skills',
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name='volunteer_skills',
    )
    skill_level = models.CharField(
        max_length=15, choices=SKILL_LEVEL_CHOICES, default=BEGINNER,
    )

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f'{self.user} - {self.skill} ({self.get_skill_level_display()})'
