from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RolePermissionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            user = request.user

            # Assuming a 'role' field exists on your user model
            user_role = getattr(user, 'role', None)

            # Allow only admins or moderators
            if user_role not in ['admin', 'moderator']:
                return JsonResponse({
                    "detail": "You do not have permission to access this resource."
                }, status=403)

        return self.get_response(request)
