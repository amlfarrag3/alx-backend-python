import logging
from datetime import datetime

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
