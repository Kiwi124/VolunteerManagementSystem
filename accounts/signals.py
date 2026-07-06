from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from accounts.audit import log_action

@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    log_action('LOGIN', f'User (ID {user.pk})', user=user)

@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    if user is not None:
        log_action('LOGOUT', f'User (ID {user.pk})', user=user)

@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, **kwargs):
    attempted_email = credentials.get('username', 'unknown')
    log_action('LOGIN_FAILED', f'Email attempted: {attempted_email}')
