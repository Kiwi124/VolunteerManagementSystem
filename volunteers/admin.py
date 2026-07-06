from django.contrib import admin

from volunteers.models import Availability, DBSStatus, Person, Skill, VolunteerSkill

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'forename', 'surname', 'phone_number', 'notification_preference')
    search_fields = ('forename', 'surname')

@admin.register(DBSStatus)
class DBSStatusAdmin(admin.ModelAdmin):
    list_display = ('dbs_status_id', 'person', 'dbs_status', 'dbs_expiry')

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('availability_id', 'user', 'day_of_week', 'start_time', 'end_time')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_id', 'skill_name')
    search_fields = ('skill_name',)

@admin.register(VolunteerSkill)
class VolunteerSkillAdmin(admin.ModelAdmin):
    list_display = ('volunteer_skill_id', 'user', 'skill', 'skill_level')
