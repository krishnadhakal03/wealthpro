import requests
import json
import datetime
import base64
import logging
from django.utils import timezone
from .models import ZoomCredentials, ZoomAvailableSlot
from django.conf import settings

logger = logging.getLogger(__name__)

def get_zoom_credentials():
    """Get the first Zoom credentials from the database"""
    creds, created = ZoomCredentials.objects.get_or_create(app_name='wealthProZoomApp')
    return creds

def get_access_token():
    """Get a valid access token for Zoom API, refreshing if necessary"""
    credentials = get_zoom_credentials()
    
    # Check if we have a valid token
    if credentials.access_token and credentials.token_expiry:
        if credentials.token_expiry > timezone.now():
            return credentials.access_token
    
    # No valid token, need to get a new one
    token_url = "https://zoom.us/oauth/token"
    
    # Encode client_id and client_secret for Basic Auth
    auth_str = f"{credentials.client_id}:{credentials.client_secret}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # If we have a refresh token, try to use it
    if credentials.refresh_token:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": credentials.refresh_token
        }
    else:
        # First time authorization
        data = {
            "grant_type": "account_credentials",
            "account_id": credentials.account_id
        }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_info = response.json()
        
        # Update credentials
        credentials.access_token = token_info.get("access_token")
        credentials.refresh_token = token_info.get("refresh_token")
        
        # Set expiry (usually 1 hour from now)
        expires_in = token_info.get("expires_in", 3600)
        credentials.token_expiry = timezone.now() + datetime.timedelta(seconds=expires_in)
        
        credentials.save()
        return credentials.access_token
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting Zoom access token: {str(e)}")
        return None

def get_user_meetings(user_id="me", start_date=None, end_date=None):
    """
    Get meetings for a Zoom user
    
    Parameters:
    - user_id: Zoom user ID (default "me" for the authenticated user)
    - start_date: Start date for filtering meetings (datetime.date)
    - end_date: End date for filtering meetings (datetime.date)
    
    Returns:
    - List of meetings
    """
    access_token = get_access_token()
    if not access_token:
        logger.error("Failed to get access token for Zoom API")
        return []
    
    # Format dates for Zoom API (YYYY-MM-DD)
    date_format = "%Y-%m-%d"
    date_params = {}
    
    if start_date:
        if isinstance(start_date, datetime.datetime):
            start_date = start_date.date()
        date_params["from"] = start_date.strftime(date_format)
    
    if end_date:
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
        date_params["to"] = end_date.strftime(date_format)
    
    # Build API URL
    api_url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    logger.info(f"Calling Zoom API: {api_url} with params: {date_params}")
    
    try:
        response = requests.get(
            api_url, 
            headers=headers, 
            params={
                "type": "scheduled",
                "page_size": 100,
                **date_params
            }
        )
        
        if not response.ok:
            logger.error(f"Zoom API error: {response.status_code} - {response.text}")
            
        response.raise_for_status()
        meetings_data = response.json()
        logger.info(f"Retrieved {len(meetings_data.get('meetings', []))} meetings from Zoom API")
        return meetings_data.get("meetings", [])
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting Zoom meetings: {str(e)}")
        return []

def create_zoom_meeting(topic, start_time, duration=60, agenda=""):
    """
    Create a Zoom meeting
    
    Parameters:
    - topic: Meeting topic/title
    - start_time: Start time (datetime.datetime in UTC)
    - duration: Duration in minutes
    - agenda: Meeting agenda/description
    
    Returns:
    - Meeting data if successful, None otherwise
    """
    access_token = get_access_token()
    if not access_token:
        logger.error("Failed to get Zoom access token")
        return None
    
    # Ensure the start_time is timezone aware and convert to UTC
    if start_time.tzinfo is None:
        start_time = timezone.make_aware(start_time)
    
    # Convert to UTC for Zoom API
    start_time_utc = start_time.astimezone(datetime.timezone.utc)
    
    # Format start_time for Zoom API (YYYY-MM-DDTHH:MM:SSZ)
    start_time_str = start_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    api_url = "https://api.zoom.us/v2/users/me/meetings"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time_str,
        "duration": duration,
        "timezone": "UTC",
        "agenda": agenda,
        "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": False,
            "waiting_room": True,
            "auto_recording": "none"
        }
    }
    
    try:
        logger.info(f"Creating Zoom meeting: {topic} at {start_time_str}")
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        
        if response.status_code != 201:
            logger.error(f"Zoom API error: {response.status_code} - {response.text}")
            return None
            
        meeting_data = response.json()
        logger.info(f"Successfully created Zoom meeting ID: {meeting_data.get('id')}")
        return meeting_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error creating Zoom meeting: {str(e)}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Failed to parse Zoom API response: {response.text}")
        return None

def sync_available_slots(start_date=None, end_date=None, days_ahead=14):
    """
    Sync available appointment slots with Zoom meetings
    
    Parameters:
    - start_date: Start date for sync (datetime.date)
    - end_date: End date for sync (datetime.date)
    - days_ahead: How many days ahead to sync if start_date/end_date not provided
    
    Returns:
    - Number of slots created/updated
    """
    # Set default date range if not provided
    if not start_date:
        start_date = timezone.now().date()
    
    if not end_date:
        end_date = start_date + datetime.timedelta(days=days_ahead)
    
    logger.info(f"Syncing Zoom slots from {start_date} to {end_date}")
    
    # Get all Zoom meetings in the date range
    meetings = get_user_meetings(start_date=start_date, end_date=end_date)
    
    if not meetings:
        logger.warning("No meetings found or error occurred when fetching meetings")
    
    # Extract existing meeting IDs for quick lookup
    existing_meeting_ids = set(
        ZoomAvailableSlot.objects.filter(meeting_id__isnull=False).values_list('meeting_id', flat=True)
    )
    
    # Mark slots that have a meeting as not available
    for meeting in meetings:
        meeting_id = meeting.get("id")
        
        # Skip if we've already processed this meeting
        if str(meeting_id) in existing_meeting_ids:
            continue
        
        # Parse meeting start time and duration
        start_time_str = meeting.get("start_time")
        duration = meeting.get("duration", 60)
        
        if not start_time_str:
            continue
        
        try:
            # Convert to UTC datetime
            start_time = datetime.datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = start_time + datetime.timedelta(minutes=duration)
            
            # Create or update slot
            ZoomAvailableSlot.objects.create(
                start_time=start_time,
                end_time=end_time,
                meeting_id=meeting_id,
                is_available=False
            )
            
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing meeting time: {str(e)}")
    
    # Create available slots for remaining times
    slots_created = 0
    
    # Business hours: 9 AM to 5 PM, 1-hour slots
    business_start_hour = 9  # 9 AM
    business_end_hour = 17   # 5 PM
    slot_duration = 60       # 60 minutes
    
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends (5=Saturday, 6=Sunday)
        if current_date.weekday() in [5, 6]:
            current_date += datetime.timedelta(days=1)
            continue
        
        # Create slots during business hours
        for hour in range(business_start_hour, business_end_hour):
            slot_start = datetime.datetime.combine(
                current_date, 
                datetime.time(hour, 0),
                tzinfo=timezone.get_current_timezone()
            )
            slot_end = slot_start + datetime.timedelta(minutes=slot_duration)
            
            # Check if this slot overlaps with any existing slots
            overlapping_slots = ZoomAvailableSlot.objects.filter(
                start_time__lt=slot_end,
                end_time__gt=slot_start
            )
            
            if not overlapping_slots.exists():
                ZoomAvailableSlot.objects.create(
                    start_time=slot_start,
                    end_time=slot_end,
                    is_available=True
                )
                slots_created += 1
        
        current_date += datetime.timedelta(days=1)
    
    logger.info(f"Created {slots_created} new available slots")
    return slots_created

def get_available_slots(start_date, end_date):
    """
    Get available slots between start_date and end_date
    
    Parameters:
    - start_date: datetime.date or string 'YYYY-MM-DD'
    - end_date: datetime.date or string 'YYYY-MM-DD'
    
    Returns:
    - List of ZoomAvailableSlot objects
    """
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Convert dates to datetime for comparison
    start_datetime = datetime.datetime.combine(
        start_date, 
        datetime.time.min, 
        tzinfo=timezone.get_current_timezone()
    )
    
    end_datetime = datetime.datetime.combine(
        end_date, 
        datetime.time.max, 
        tzinfo=timezone.get_current_timezone()
    )
    
    # Get slots that are available and in the future
    now = timezone.now()
    available_slots = ZoomAvailableSlot.objects.filter(
        is_available=True,
        start_time__gte=now,
        start_time__lte=end_datetime
    ).order_by('start_time')
    
    return available_slots

def book_appointment_slot(slot_id, name, email, phone=None, notes=None):
    """
    Book an appointment and create a Zoom meeting
    
    Parameters:
    - slot_id: ID of the ZoomAvailableSlot to book
    - name: Client name
    - email: Client email
    - phone: Client phone number
    - notes: Additional notes
    
    Returns:
    - Tuple of (success, meeting_data or error message)
    """
    try:
        slot = ZoomAvailableSlot.objects.get(id=slot_id, is_available=True)
    except ZoomAvailableSlot.DoesNotExist:
        return False, "The selected time slot is no longer available."
    
    # Create Zoom meeting
    meeting_topic = f"Next Generation Wealth Pro Appointment with {name}"
    agenda = f"Appointment with {name}. Contact info: {email}"
    if phone:
        agenda += f", {phone}"
    if notes:
        agenda += f". Notes: {notes}"
    
    meeting_data = create_zoom_meeting(
        topic=meeting_topic,
        start_time=slot.start_time,
        duration=(slot.end_time - slot.start_time).total_seconds() // 60,
        agenda=agenda
    )
    
    if not meeting_data:
        return False, "Failed to create Zoom meeting. Please try again."
    
    # Update slot with meeting info
    slot.is_available = False
    slot.meeting_id = meeting_data.get("id")
    slot.save()
    
    logger.info(f"Booked appointment slot {slot_id} for {name} ({email})")
    
    return True, meeting_data

def mark_slot_unavailable(slot_id):
    """
    Mark a Zoom slot as unavailable after it's been booked
    
    Parameters:
    - slot_id: ID of the ZoomAvailableSlot
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        slot = ZoomAvailableSlot.objects.get(id=slot_id)
        slot.is_available = False
        slot.save()
        logger.info(f"Marked slot {slot_id} as unavailable")
        return True
    except ZoomAvailableSlot.DoesNotExist:
        logger.error(f"Slot with ID {slot_id} not found")
        return False
    except Exception as e:
        logger.error(f"Error marking slot {slot_id} as unavailable: {str(e)}")
        return False 