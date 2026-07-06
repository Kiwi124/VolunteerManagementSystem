from django.core.management.base import BaseCommand

from programmes.models import Status

STATUS_NAMES = ['Planned', 'Active', 'Completed', 'Cancelled']


class Command(BaseCommand):
    help = 'Seeds the shared Status lookup table used by Programme and Event.'

    def handle(self, *args, **options):
        for status_name in STATUS_NAMES:
            Status.objects.get_or_create(status=status_name)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(STATUS_NAMES)} statuses.'))
