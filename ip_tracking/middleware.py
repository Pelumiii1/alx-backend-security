from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden('<h1>Forbidden</h1><p>Your IP address has been blocked.</p>')

        path = request.path
        RequestLog.objects.create(ip_address=ip_address, path=path)
        response = self.get_response(request)
        return response
