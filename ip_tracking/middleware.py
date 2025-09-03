from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
from django.core.cache import cache

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden('<h1>Forbidden</h1><p>Your IP address has been blocked.</p>')

        path = request.path

        geolocation = cache.get(ip_address)
        if not geolocation:
            try:
                geolocation = request.ip_geolocation
                cache.set(ip_address, geolocation, 60 * 60 * 24)
            except AttributeError:
                geolocation = { 'country': 'Unknown', 'city': 'Unknown' }

        RequestLog.objects.create(
            ip_address=ip_address, 
            path=path,
            country=geolocation.get('country', 'Unknown'),
            city=geolocation.get('city', 'Unknown')
        )

        response = self.get_response(request)
        return response
