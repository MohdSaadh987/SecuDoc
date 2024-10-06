# fmsApp/middleware.py

from django.utils.deprecation import MiddlewareMixin

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/shareF/'):
            response['X-Frame-Options'] = 'ALLOWALL'
        return response
