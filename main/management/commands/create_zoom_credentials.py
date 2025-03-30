from django.core.management.base import BaseCommand
from main.models import ZoomCredentials

class Command(BaseCommand):
    help = 'Creates initial Zoom API credentials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating initial Zoom credentials...'))
        
        credentials, created = ZoomCredentials.objects.get_or_create(
            app_name='wealthProZoomApp',
            defaults={
                'account_id': 'Sn2rpXqFRmC7AitP028Xmg',
                'client_id': 'FC0NGNG7QfyRU7yLXHCrMw',
                'client_secret': '68kBbdAS49mzxtvQebGl1BM5fzN6AgBp',
                'secret_token': 'Hapqqa_CRN2HzdT0R-kgiw',
                'verification_token': 'TdcWSKzkSV6J3PBjo1qVpQ'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Zoom credentials'))
        else:
            self.stdout.write(self.style.SUCCESS('Zoom credentials already exist')) 