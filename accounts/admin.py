from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AuditLog, Role, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'person', 'role', 'user_status')
    list_filter = ('role', 'user_status')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'person', 'role', 'user_status')}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'person', 'role', 'password1', 'password2')}),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('audit_id', 'timestamp', 'user', 'action_performed', 'entity_affected')
    readonly_fields = ('audit_id', 'user', 'action_performed', 'entity_affected', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
