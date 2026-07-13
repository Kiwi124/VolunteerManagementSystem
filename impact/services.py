from datetime import timedelta

from django.db.models import Avg, Sum
from django.utils import timezone

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

COST_RANGE_CHOICES = [
    ('all', 'All time'),
    ('1m', 'Last month'),
    ('3m', 'Last 3 months'),
    ('6m', 'Last 6 months'),
    ('1y', 'Last year'),
    ('custom', 'Custom range'),
]

COST_RANGE_DAYS = {
    '1m': 30,
    '3m': 90,
    '6m': 182,
    '1y': 365,
}

def resolve_cost_window(range_key, custom_start=None, custom_end=None):
    if range_key == 'custom':
        return custom_start, custom_end
    if range_key in COST_RANGE_DAYS:
        today = timezone.localdate()
        return today - timedelta(days=COST_RANGE_DAYS[range_key]), today
    return None, None

def total_programme_cost(start=None, end=None):
    programmes = Programme.objects.all()
    if start is not None:
        programmes = programmes.filter(start_date__gte=start)
    if end is not None:
        programmes = programmes.filter(start_date__lte=end)
    return programmes.aggregate(total=Sum('programme_cost'))['total'] or 0
