from django.conf import settings
from django.db import models

from volunteers.models import Skill


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.status


class Programme(models.Model):
    programme_id = models.AutoField(primary_key=True)
    programme_name = models.CharField(max_length=150)
    programme_description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='programmes')
    programme_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.programme_name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='events')
    event_description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name='events')
    capacity = models.PositiveIntegerField()
    required_skills = models.ManyToManyField(Skill, through='EventSkill', related_name='events')

    def __str__(self):
        return f'{self.programme.programme_name} - {self.start_date:%Y-%m-%d}'


class EventSkill(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='event_skills')

    class Meta:
        unique_together = ('event', 'skill')

    def __str__(self):
        return f'{self.event} requires {self.skill}'


class VolunteerAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments',
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='assignments')
    volunteer_role = models.CharField(max_length=100, blank=True)
    attendance = models.BooleanField(default=False)
    assignment_date = models.DateField(auto_now_add=True)
    notify_flag = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user} -> {self.event}'
