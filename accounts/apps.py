from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from accounts.audit import register_audit_logging
        from accounts.models import Role, User
        import accounts.signals

        register_audit_logging(User, 'User')
        register_audit_logging(Role, 'Role')
