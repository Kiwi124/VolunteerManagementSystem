import logging

from django.core.mail import send_mail

from volunteers.models import Person

logger = logging.getLogger('notifications')

def send_notification(person, subject, message):
    if person.notification_preference == Person.NOTIFY_EMAIL:
        user_account = getattr(person, 'user_account', None)
        if user_account is None:
            logger.warning('No email available for %s, skipping notification.', person)
            return
        send_mail(subject, message, None, [user_account.email])
    elif person.notification_preference in (Person.NOTIFY_SMS, Person.NOTIFY_PHONE):
        logger.info(
            'Simulated %s to %s (%s): %s',
            person.get_notification_preference_display(), person, person.phone_number, message,
        )
    # NOTIFY_NONE: the person has opted out, do nothing.
