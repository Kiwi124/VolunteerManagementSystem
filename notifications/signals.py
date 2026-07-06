from programmes.models import VolunteerAssignment

from notifications.services import send_notification

def on_assignment_created(sender, instance, created, **kwargs):
    if not created:
        return
    send_notification(
        instance.user.person,
        subject='You have been assigned to an event',
        message=(
            f'You have been assigned to "{instance.event}" as {instance.volunteer_role or "a volunteer"}. '
            f'Starts {instance.event.start_date:%d %b %Y %H:%M}.'
        ),
    )

def connect():
    from django.db.models.signals import post_save
    post_save.connect(on_assignment_created, sender=VolunteerAssignment, weak=False)
