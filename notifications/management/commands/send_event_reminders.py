from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from notifications.services import send_notification
from programmes.models import VolunteerAssignment

class Command(BaseCommand):
    help = (
        'Sends a reminder to volunteers whose assigned event starts within the next N hours '
        'and have not already been reminded (notifyFlag).'
    )

    def add_arguments(self, parser):
        parser.add_argument('--hours', type=int, default=24, help='Reminder window in hours (default 24).')

    def handle(self, *args, **options):
        now = timezone.now()
        window_end = now + timedelta(hours=options['hours'])

        due = VolunteerAssignment.objects.filter(
            notify_flag=False,
            event__start_date__gte=now,
            event__start_date__lte=window_end,
        ).select_related('user__person', 'event')

        sent = 0
        for assignment in due:
            send_notification(
                assignment.user.person,
                subject='Reminder: upcoming volunteering event',
                message=(
                    f'Reminder: "{assignment.event}" starts '
                    f'{assignment.event.start_date:%d %b %Y %H:%M}.'
                ),
            )
            assignment.notify_flag = True
            assignment.save(update_fields=['notify_flag'])
            sent += 1

        self.stdout.write(self.style.SUCCESS(f'Sent {sent} reminder(s).'))
