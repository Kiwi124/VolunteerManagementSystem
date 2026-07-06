from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def role_required(*role_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(request, *args, **kwargs):
            user_role = getattr(request.user.role, 'role_name', None)
            if user_role not in role_names:
                raise PermissionDenied('You do not have access to this page.')
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
