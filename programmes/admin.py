from django.contrib import admin

from programmes.models import Event, EventSkill, Programme, Status, VolunteerAssignment

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status_id', 'status')

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('programme_id', 'programme_name', 'status', 'start_date', 'end_date', 'programme_cost')
    list_filter = ('status',)

class EventSkillInline(admin.TabularInline):
    model = EventSkill
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'programme', 'start_date', 'end_date', 'status', 'capacity')
    list_filter = ('status', 'programme')
    inlines = [EventSkillInline]

@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'user', 'event', 'volunteer_role', 'attendance', 'notify_flag')
    list_filter = ('attendance', 'notify_flag')
