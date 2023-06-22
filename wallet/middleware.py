import logging

logger = logging.getLogger(__name__)

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
    
        # Log 400 and 500 response codes
        if response.status_code >= 400:
            logger.error(f"Response Code: {response.status_code}")

        return response
