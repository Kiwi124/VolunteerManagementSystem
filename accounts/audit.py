import threading

from django.db.models.signals import post_delete, post_save

_thread_locals = threading.local()

def set_current_user(user):
    _thread_locals.user = user

def get_current_user():
    return getattr(_thread_locals, 'user', None)

def log_action(action_performed, entity_affected, user=None):
    from accounts.models import AuditLog

    AuditLog.objects.create(
        user=user if user is not None else get_current_user(),
        action_performed=action_performed,
        entity_affected=entity_affected,
    )

def register_audit_logging(model, label):
    def _on_save(sender, instance, created, update_fields=None, **kwargs):
        if not created and update_fields and set(update_fields) == {'last_login'}:
            return
        action = 'CREATED' if created else 'UPDATED'
        log_action(action, f'{label} (ID {instance.pk})')

    def _on_delete(sender, instance, **kwargs):
        log_action('DELETED', f'{label} (ID {instance.pk})')

    post_save.connect(_on_save, sender=model, weak=False)
    post_delete.connect(_on_delete, sender=model, weak=False)
