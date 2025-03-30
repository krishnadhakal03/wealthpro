from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
import logging
from main.models import ZoomAvailableSlot
from main.zoom_utils import sync_available_slots

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean up old Zoom slots and refresh available slots'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=14,
            help='Number of days ahead to sync (default: 14)'
        )
        parser.add_argument(
            '--keep-days',
            type=int,
            default=7,
            help='Number of days of past slots to keep (default: 7)'
        )

    def handle(self, *args, **options):
        days_ahead = options['days']
        keep_days = options['keep_days']
        
        self.stdout.write(self.style.SUCCESS(f'Starting Zoom slot cleanup...'))
        
        # Delete old slots
        cutoff_date = timezone.now() - datetime.timedelta(days=keep_days)
        
        old_slots = ZoomAvailableSlot.objects.filter(
            start_time__lt=cutoff_date
        )
        
        count = old_slots.count()
        old_slots.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} old Zoom slots.'))
        
        # Clear unavailable slots without meetings
        unavailable_slots = ZoomAvailableSlot.objects.filter(
            is_available=False, 
            meeting_id__isnull=True
        )
        
        count = unavailable_slots.count()
        unavailable_slots.delete()
        
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} unavailable slots without meetings.'))
        
        # Sync new slots
        slots_created = sync_available_slots(
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + datetime.timedelta(days=days_ahead),
            days_ahead=days_ahead
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created {slots_created} new available slots.')) 