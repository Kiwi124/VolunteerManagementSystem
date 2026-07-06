from django.apps import AppConfig

class ImpactConfig(AppConfig):
    name = 'impact'

    def ready(self):
        from accounts.audit import register_audit_logging
        from impact.models import Report

        register_audit_logging(Report, 'Report')
