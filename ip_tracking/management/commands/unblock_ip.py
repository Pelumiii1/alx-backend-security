from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Unblocks an IP address by removing it from the BlockedIP list.'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to unblock.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        try:
            blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
            blocked_ip.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully unblocked IP address {ip_address}.'))
        except BlockedIP.DoesNotExist:
            self.stdout.write(self.style.WARNING(f'IP address {ip_address} is not blocked.'))
