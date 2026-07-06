from accounts.audit import set_current_user

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        set_current_user(user if user and user.is_authenticated else None)
        try:
            response = self.get_response(request)
        finally:
            set_current_user(None)
        return response
