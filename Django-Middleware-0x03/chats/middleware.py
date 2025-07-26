import logging
from datetime import datetime , timedelta
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
from django.http import JsonResponse

logger = logging.getLogger(__name__)
handler = logging.FileHandler('request_logs.log')  # Logs to a file in the project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = now.replace(hour=18, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=21, minute=0, second=0, microsecond=0)

        # Allow access only between 6PM and 9PM
        if not (start_time <= now <= end_time):
            return HttpResponseForbidden(
                "<h1>Access Forbidden</h1><p>Chat access is only allowed between 6PM and 9PM.</p>"
            )

        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to store IP request timestamps
        self.ip_message_log = defaultdict(list)
        self.limit = 5  # 5 messages
        self.time_window = timedelta(minutes=1)  # 1 minute window

    def __call__(self, request):
        if request.method == 'POST' and '/messages' in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Clean up old timestamps
            recent_requests = [
                t for t in self.ip_message_log[ip]
                if now - t < self.time_window
            ]
            self.ip_message_log[ip] = recent_requests

            if len(recent_requests) >= self.limit:
                return JsonResponse({
                    "detail": "Rate limit exceeded. Max 5 messages per minute allowed."
                }, status=429)

            # Add current timestamp
            self.ip_message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware(MiddlewareMixin):
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


