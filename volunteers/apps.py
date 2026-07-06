from django.apps import AppConfig

class VolunteersConfig(AppConfig):
    name = 'volunteers'

    def ready(self):
        from accounts.audit import register_audit_logging
        from volunteers.models import Availability, DBSStatus, Person, Skill, VolunteerSkill

        register_audit_logging(Person, 'Person details')
        register_audit_logging(DBSStatus, 'DBS status')
        register_audit_logging(Availability, 'Availability')
        register_audit_logging(Skill, 'Skill')
        register_audit_logging(VolunteerSkill, 'Volunteer skill')
