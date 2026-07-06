from django.db.models import Avg

from accounts.models import Role, User
from impact.models import Report
from programmes.models import Event, Programme, VolunteerAssignment

def programme_metrics(programme):
    assignments = VolunteerAssignment.objects.filter(event__programme=programme)
    total_assignments = assignments.count()
    attended = assignments.filter(attendance=True).count()
    return {
        'events_count': programme.events.count(),
        'total_assignments': total_assignments,
        'attended_count': attended,
        'attendance_rate': round((attended / total_assignments) * 100, 1) if total_assignments else 0,
        'unique_volunteers': assignments.values('user').distinct().count(),
    }

def organisation_metrics():
    total_assignments = VolunteerAssignment.objects.count()
    attended = VolunteerAssignment.objects.filter(attendance=True).count()
    return {
        'total_programmes': Programme.objects.count(),
        'total_events': Event.objects.count(),
        'total_volunteers': User.objects.filter(role__role_name=Role.VOLUNTEER).count(),
        'total_assignments': total_assignments,
        'attendance_rate': round((attended / total_assignments) * 100, 1) if total_assignments else 0,
        'average_satisfaction': round(Report.objects.aggregate(avg=Avg('satisfaction_score'))['avg'] or 0, 1),
    }
