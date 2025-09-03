from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP
from django.db.models import Count

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # IPs with more than 100 requests in the last hour
    suspicious_ips_by_requests = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for item in suspicious_ips_by_requests:
        SuspiciousIP.objects.get_or_create(
            ip_address=item['ip_address'],
            defaults={'reason': f'Exceeded 100 requests in the last hour. Count: {item["request_count"]}'}
        )

    # IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login']
    suspicious_ips_by_path = (
        RequestLog.objects.filter(path__in=sensitive_paths, timestamp__gte=one_hour_ago)
        .values('ip_address')
        .distinct()
    )

    for item in suspicious_ips_by_path:
        SuspiciousIP.objects.get_or_create(
            ip_address=item['ip_address'],
            defaults={'reason': 'Accessed a sensitive path.'}
        )
