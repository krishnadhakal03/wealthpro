import os
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
from main.zoom_utils import sync_available_slots

class Command(BaseCommand):
    help = 'Sync available Zoom slots with existing meetings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=14,
            help='Number of days ahead to sync (default: 14)'
        )

    def handle(self, *args, **options):
        days_ahead = options['days']
        
        self.stdout.write(self.style.SUCCESS(f'Starting Zoom slot sync for {days_ahead} days ahead...'))
        
        start_date = timezone.now().date()
        end_date = start_date + datetime.timedelta(days=days_ahead)
        
        slots_created = sync_available_slots(start_date, end_date, days_ahead)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully synced Zoom slots. Created {slots_created} new available slots.')) 