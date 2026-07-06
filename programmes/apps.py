from django.apps import AppConfig


class ProgrammesConfig(AppConfig):
    name = 'programmes'

    def ready(self):
        from accounts.audit import register_audit_logging
        from programmes.models import Event, Programme, VolunteerAssignment

        register_audit_logging(Programme, 'Programme')
        register_audit_logging(Event, 'Event')
        register_audit_logging(VolunteerAssignment, 'Volunteer assignment')
