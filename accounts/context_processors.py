from accounts.models import Role

def role_groups(request):
    return {
        'volunteer_manager_roles': [
            Role.ADMIN,
            Role.PROGRAMME_COORDINATOR,
            Role.VOLUNTEER_COORDINATOR,
            Role.OPERATIONS_MANAGER,
        ],
        'programme_manager_roles': [
            Role.ADMIN,
            Role.OPERATIONS_MANAGER,
            Role.PROGRAMME_COORDINATOR,
        ],
        'impact_manager_roles': [
            Role.ADMIN,
            Role.FUNDER_RELATIONS_MANAGER,
        ],
        'dashboard_viewer_roles': [
            Role.ADMIN,
            Role.FUNDER_RELATIONS_MANAGER,
            Role.OPERATIONS_MANAGER,
            Role.PROGRAMME_COORDINATOR,
        ],
    }
