from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.views.decorators.http import require_POST
import json
import datetime
import logging
from django.db import models
from decimal import Decimal

from main.forms import ContactForm, AppointmentForm
from main.models import (
    Videos, HomeInfoSection, HomeSliderImage, Team, 
    ServicesSection, BusinessContact, Contactus, 
    Appointment, VideoDirect, ZoomAvailableSlot, 
    InsuranceType, InsuranceBaseRate, InsuranceInvestmentReturn,
    StateRateAdjustment, CSOMortalityTable, InsuranceRiskFactor, RiskFactorValue,
    DisclaimerText, StateRegulation
)
from .zoom_utils import (
    sync_available_slots, get_available_slots, 
    book_appointment_slot, create_zoom_meeting, mark_slot_unavailable
)
from main.settings_service import get_maps_settings, get_business_hours

# Create your views here.

logger = logging.getLogger(__name__)

# Helper function for insurance calculator
def get_age_bracket(age):
    """
    Returns the appropriate age bracket for insurance calculations based on age.
    """
    if age < 18:
        return "0-17"
    elif age <= 29:
        return "18-29"
    elif age <= 39:
        return "30-39"
    elif age <= 49:
        return "40-49"
    elif age <= 59:
        return "50-59"
    elif age <= 69:
        return "60-69"
    else:
        return "70+"
        
# Helper function for maturity value calculation
def calculate_maturity_value(premium, years, annual_return_rate):
    """
    Calculate the maturity value of an investment based on annual premium, 
    years, and annual return rate.
    """
    maturity_value = Decimal('0')
    annual_rate = Decimal(str(annual_return_rate)) / Decimal('100')
    
    for year in range(1, int(years) + 1):
        # Add this year's premium
        maturity_value += premium
        # Apply return rate to current total
        maturity_value = maturity_value * (Decimal('1') + annual_rate)
        
    return maturity_value

# Helper function for premium calculation
def calculate_premium(base_rate, coverage_amount, term_years, insurance_type, age, gender, request_data):
    """
    Calculate insurance premium based on base rate and other factors
    """
    monthly_premium = (base_rate * coverage_amount) / 1000 / 12
    
    # Apply term length factor
    if insurance_type.name.lower() == 'life':
        # Life insurance has different term factors
        if term_years <= 5:
            term_factor = 1.0
        elif term_years <= 10:
            term_factor = 0.95
        elif term_years <= 20:
            term_factor = 0.9
        else:
            term_factor = 0.85
    else:
        # Other insurance types
        if term_years < 1:
            term_factor = 1.1  # 6 month policies have 10% surcharge
        elif term_years == 1:
            term_factor = 1.0
        else:
            term_factor = 0.9  # Multi-year policies get 10% discount
            
    monthly_premium *= Decimal(str(term_factor))
    
    # Apply risk factors based on insurance type
    insurance_type_name = insurance_type.name.lower()
    
    if insurance_type_name == 'life':
        # Smoker status
        smoker_status = request_data.get('smoker_status', 'NS')
        if smoker_status == 'Occasional':
            monthly_premium *= Decimal('1.25')
        elif smoker_status == 'Regular':
            monthly_premium *= Decimal('1.75')
        elif smoker_status == 'Heavy':
            monthly_premium *= Decimal('2.5')
            
        # BMI category
        bmi_category = request_data.get('bmi_category', 'Normal')
        if bmi_category == 'Overweight':
            monthly_premium *= Decimal('1.15')
        elif bmi_category == 'Obese':
            monthly_premium *= Decimal('1.5')
        elif bmi_category == 'Severely obese':
            monthly_premium *= Decimal('2.0')
            
        # Family history
        family_history = request_data.get('family_history', 'None')
        if family_history == 'Cancer':
            monthly_premium *= Decimal('1.25')
        elif family_history == 'Heart':
            monthly_premium *= Decimal('1.3')
        elif family_history == 'Diabetes':
            monthly_premium *= Decimal('1.2')
        elif family_history == 'Multiple':
            monthly_premium *= Decimal('1.5')
            
        # Occupation risk
        occupation_risk = request_data.get('occupation_risk', 'Low')
        if occupation_risk == 'Moderate':
            monthly_premium *= Decimal('1.1')
        elif occupation_risk == 'High':
            monthly_premium *= Decimal('1.35')
        elif occupation_risk == 'Very high':
            monthly_premium *= Decimal('1.75')
            
    elif insurance_type_name == 'health':
        # Pre-existing conditions
        health_condition = request_data.get('health_condition', 'None')
        if health_condition == 'Diabetes':
            monthly_premium *= Decimal('1.35')
        elif health_condition == 'Hypertension':
            monthly_premium *= Decimal('1.25')
        elif health_condition == 'Heart Disease':
            monthly_premium *= Decimal('1.65')
        elif health_condition == 'Cancer':
            monthly_premium *= Decimal('1.75')
        elif health_condition == 'Multiple':
            monthly_premium *= Decimal('2.0')
            
        # Lifestyle
        lifestyle = request_data.get('lifestyle', 'Good')
        if lifestyle == 'Excellent':
            monthly_premium *= Decimal('0.9')
        elif lifestyle == 'Fair':
            monthly_premium *= Decimal('1.15')
        elif lifestyle == 'Poor':
            monthly_premium *= Decimal('1.35')
            
        # Prescription medications
        prescription_meds = request_data.get('prescription_meds', 'None')
        if prescription_meds == '1-2':
            monthly_premium *= Decimal('1.15')
        elif prescription_meds == '3-5':
            monthly_premium *= Decimal('1.35')
        elif prescription_meds == 'More than 5':
            monthly_premium *= Decimal('1.75')
            
        # Coverage level
        coverage_level = request_data.get('coverage_level', 'Silver')
        if coverage_level == 'Bronze':
            monthly_premium *= Decimal('0.8')
        elif coverage_level == 'Gold':
            monthly_premium *= Decimal('1.2')
        elif coverage_level == 'Platinum':
            monthly_premium *= Decimal('1.5')
            
    elif insurance_type_name == 'auto':
        # Vehicle type
        vehicle_type = request_data.get('vehicle_type', 'Mid-size')
        if vehicle_type == 'Economy':
            monthly_premium *= Decimal('0.9')
        elif vehicle_type == 'SUV':
            monthly_premium *= Decimal('1.2')
        elif vehicle_type == 'Luxury':
            monthly_premium *= Decimal('1.5')
        elif vehicle_type == 'Sports':
            monthly_premium *= Decimal('1.7')
        elif vehicle_type == 'High-performance':
            monthly_premium *= Decimal('2.0')
            
        # Driving record
        driving_record = request_data.get('driving_record', 'Clean')
        if driving_record == 'Minor':
            monthly_premium *= Decimal('1.25')
        elif driving_record == 'Major':
            monthly_premium *= Decimal('1.75')
        elif driving_record == 'DUI':
            monthly_premium *= Decimal('2.5')
        elif driving_record == 'Multiple':
            monthly_premium *= Decimal('3.0')
            
        # Annual mileage
        annual_mileage = request_data.get('annual_mileage', '5000-10000')
        if annual_mileage == 'Under 5000':
            monthly_premium *= Decimal('0.85')
        elif annual_mileage == '10001-15000':
            monthly_premium *= Decimal('1.1')
        elif annual_mileage == '15001-20000':
            monthly_premium *= Decimal('1.25')
        elif annual_mileage == 'Over 20000':
            monthly_premium *= Decimal('1.4')
            
        # Vehicle age
        vehicle_age = request_data.get('vehicle_age', 'Recent')
        if vehicle_age == 'New':
            monthly_premium *= Decimal('1.2')
        elif vehicle_age == 'Older':
            monthly_premium *= Decimal('0.9')
        elif vehicle_age == 'Vintage':
            monthly_premium *= Decimal('0.8')
            
    elif insurance_type_name == 'home':
        # Construction type
        construction_type = request_data.get('construction_type', 'Wood')
        if construction_type == 'Brick':
            monthly_premium *= Decimal('0.9')
        elif construction_type == 'Steel':
            monthly_premium *= Decimal('0.85')
        elif construction_type == 'Mixed':
            monthly_premium *= Decimal('0.95')
            
        # Roof age
        roof_age = request_data.get('roof_age', 'Mid')
        if roof_age == 'New':
            monthly_premium *= Decimal('0.9')
        elif roof_age == 'Older':
            monthly_premium *= Decimal('1.25')
        elif roof_age == 'Very old':
            monthly_premium *= Decimal('1.6')
            
        # Location risk
        location_risk = request_data.get('location_risk', 'Low')
        if location_risk == 'Moderate':
            monthly_premium *= Decimal('1.25')
        elif location_risk == 'Flood':
            monthly_premium *= Decimal('1.75')
        elif location_risk == 'Wildfire':
            monthly_premium *= Decimal('1.9')
        elif location_risk == 'Hurricane':
            monthly_premium *= Decimal('2.0')
        elif location_risk == 'Multiple':
            monthly_premium *= Decimal('2.5')
            
        # Security features
        security_features = request_data.get('security_features', 'Basic')
        if security_features == 'Comprehensive':
            monthly_premium *= Decimal('0.8')
        elif security_features == 'Minimal':
            monthly_premium *= Decimal('1.15')
        elif security_features == 'None':
            monthly_premium *= Decimal('1.3')
            
    return monthly_premium

def home(request):
    info_sections = HomeInfoSection.objects.all()
    slider_images = HomeSliderImage.objects.all()
    context = {
        'info_sections': info_sections,
        'slider_images': slider_images,
        'MEDIA_URL': settings.MEDIA_URL,  # Add MEDIA_URL to context if needed
    }
    return render(request, "main/home.html", context)

def team(request):
    teams = Team.objects.all()
    return render(request, "main/team.html", {"teams": teams})

def videos(request):
    vid = Videos.objects.all()
    directVideo = VideoDirect.objects.all()
    return render(request, "main/videos.html", {"vid": vid, "directVideo": directVideo})

def appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            addressline2 = form.cleaned_data.get('addressline2', '')
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            appointment_date = form.cleaned_data['appointment']
            
            # Check if we have a selected Zoom slot
            zoom_slot_id = request.POST.get('zoom_slot_id')
            
            if zoom_slot_id:
                try:
                    # Get the selected slot
                    zoom_slot = ZoomAvailableSlot.objects.get(id=zoom_slot_id, is_available=True)
                    
                    # Book the Zoom meeting
                    success, meeting_data = book_appointment_slot(
                        slot_id=zoom_slot_id,
                        name=name,
                        email=email,
                        phone=phone,
                        notes=f"Address: {address}, {city}, {state} {zipcode}, {country}"
                    )
                    
                    if success:
                        # Create appointment with Zoom details
                        if zoom_slot and meeting_data:
                            # Create a new appointment with Zoom details
                            appointment = Appointment(
                                name=name,
                                phone=phone,
                                email=email,
                                address=address,
                                addressline2=addressline2 or None,
                                city=city,
                                zipcode=zipcode,
                                state=state,
                                country=country,
                                meetingDate=zoom_slot.start_time.date(),
                                meetingTime=zoom_slot.start_time.time(),
                                meetingUrl=meeting_data.get('join_url'),
                                zoom_slot=zoom_slot,
                                zoom_meeting_id=meeting_data.get('id'),
                                zoom_meeting_url=meeting_data.get('join_url'),
                                zoom_meeting_password=meeting_data.get('password'),
                            )
                            appointment.save()
                            
                            # Mark the slot as unavailable
                            mark_slot_unavailable(zoom_slot.id)
                            
                            logger.info(f"Created Zoom appointment for {name} with meeting ID: {meeting_data.get('id')}")
                            
                            # Send email with Zoom details
                            subject = f"Your Zoom Appointment Confirmation - {name}"
                            message = f"""
                                Your appointment has been scheduled!
                                
                                Date: {zoom_slot.start_time.strftime('%A, %B %d, %Y')}
                                Time: {zoom_slot.start_time.strftime('%I:%M %p')} - {zoom_slot.end_time.strftime('%I:%M %p')}
                                
                                Zoom Meeting Link: {meeting_data.get('join_url')}
                                Meeting ID: {meeting_data.get('id')}
                                Password: {meeting_data.get('password', 'No password required')}
                                
                                Please click the Zoom link a few minutes before your scheduled time.
                                If you need to reschedule, please contact us as soon as possible.
                                
                                Thank you for choosing Next Generation Wealth Pro!
                                """
                            
                            # Send to customer
                            try:
                                send_mail(
                                    subject,
                                    message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    [email],
                                    fail_silently=False,
                                )
                            except Exception as e:
                                logger.error(f"Failed to send confirmation email to customer: {str(e)}")
                            
                            # Send notification to admin
                            admin_subject = f"New Zoom Appointment - {name}"
                            admin_message = f"""
                                A new Zoom appointment has been scheduled:
                                
                                Client: {name}
                                Phone: {phone}
                                Email: {email}
                                Date: {zoom_slot.start_time.strftime('%A, %B %d, %Y')}
                                Time: {zoom_slot.start_time.strftime('%I:%M %p')} - {zoom_slot.end_time.strftime('%I:%M %p')}
                                
                                Zoom Meeting ID: {meeting_data.get('id')}
                                Zoom Meeting Link: {meeting_data.get('join_url')}
                                """
                            
                            try:
                                send_mail(
                                    admin_subject,
                                    admin_message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    [settings.CONTACT_EMAIL],
                                    fail_silently=False,
                                )
                            except Exception as e:
                                logger.error(f"Failed to send admin notification email: {str(e)}")
                            
                            messages.success(request, "Your Zoom appointment has been scheduled successfully! Check your email for details.")
                            
                            # Pass Zoom meeting details to the template
                            zoom_meeting = {
                                'join_url': meeting_data.get('join_url'),
                                'id': meeting_data.get('id'),
                                'password': meeting_data.get('password')
                            }
                            
                            return render(request, "main/appointment.html", {
                                "form": form, 
                                "success": True,
                                "zoom_meeting": zoom_meeting
                            })
                        else:
                            # If either the zoom slot wasn't found or the meeting creation failed
                            logger.error(f"Failed to create Zoom appointment: slot_found={zoom_slot is not None}, meeting_created={meeting_data is not None}")
                            if not zoom_slot:
                                messages.error(request, "Sorry, this time slot is no longer available. Please select another time.")
                            else:
                                messages.error(request, "We encountered an issue creating your Zoom meeting. Please try again or contact us directly.")
                            
                            # Still create a regular appointment
                            appointment = Appointment(
                                name=name,
                                phone=phone,
                                email=email,
                                address=address,
                                addressline2=addressline2 or None,
                                city=city,
                                zipcode=zipcode,
                                state=state,
                                country=country,
                                appointment=appointment_date,
                                status='request'
                            )
                            appointment.save()
                            logger.info(f"Created traditional appointment as fallback for {name}")
                            
                            # Send notification to admin
                            subject = "Appointment Request (Zoom Failed)"
                            message = f"""
                            New appointment request (Zoom meeting creation failed):
                            
                            Name: {name}
                            Phone: {phone}
                            Email: {email}
                            Address: {address} {addressline2 or ''}
                            {city}, {state} {zipcode}
                            Country: {country}

                            Date of appointment:
                            {appointment_date}
                            """
                            
                            try:
                                send_mail(
                                    subject,
                                    message,
                                    settings.DEFAULT_FROM_EMAIL,
                                    [settings.CONTACT_EMAIL],
                                    fail_silently=False,
                                )
                            except Exception as e:
                                logger.error(f"Failed to send admin notification for traditional appointment: {str(e)}")
                            
                            messages.success(request, "Your appointment request has been received. We will contact you shortly to confirm.")
                            return render(request, "main/appointment.html", {"form": form, "success": True})
                except ZoomAvailableSlot.DoesNotExist:
                    messages.error(request, "The selected time slot is no longer available.")
                    return render(request, "main/appointment.html", {"form": form})
                except Exception as e:
                    logger.error(f"Error creating Zoom appointment: {str(e)}")
                    messages.error(request, f"Error creating appointment: {str(e)}")
                    return render(request, "main/appointment.html", {"form": form})
            
            # Traditional appointment processing (no Zoom)
            try:
                # Check if we have an appointment date
                appointment_date = form.cleaned_data.get('appointment')

                # Prepare the email content
                subject = f"New Appointment request - {name}"
                message = f"""
                You have received a new appointment request from {name}. 

                Phone: {phone}
                Email: {email}
                Address: {address}
                Addressline2: {addressline2 if addressline2 else 'N/A'}
                City: {city}
                Zipcode: {zipcode}
                State: {state}
                Country: {country}
                """
                
                # Add appointment date information if provided
                if appointment_date:
                    message += f"""
                    Preferred date:
                    {appointment_date}
                    """
                else:
                    message += """
                    No specific date requested. The client has selected "contact me to arrange a time."
                    """

                # Send the email to your email address (configured in settings.py)
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,  # Use the default email configured in settings
                        [settings.CONTACT_EMAIL],  # Use contact email from settings
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.error(f"Failed to send email for traditional appointment: {str(e)}")

                # Save the appointment to the database
                appointment = Appointment(
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                    addressline2=addressline2 or None,
                    city=city,
                    zipcode=zipcode,
                    state=state,
                    country=country,
                    appointment=appointment_date,
                    status='request'
                )
                appointment.save()
                
                logger.info(f"Created traditional appointment for {name} on {appointment_date if appointment_date else 'no date specified'}")

                # Also send confirmation to the customer
                try:
                    customer_subject = "Your Appointment Request - Next Generation Wealth Pro"
                    customer_message = f"""
                        Thank you for your appointment request!
                        
                        We have received your request for an appointment on {appointment_date}.
                        
                        Our team will review your request and contact you shortly to confirm the details.
                        
                        Thank you for choosing Next Generation Wealth Pro!
                        """
                    
                    send_mail(
                        customer_subject,
                        customer_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.error(f"Failed to send confirmation email to customer: {str(e)}")

                return render(request, "main/appointment.html",
                              {"form": form, "success": True})
            except Exception as e:
                logger.error(f"Error creating traditional appointment: {str(e)}")
                messages.error(request, f"Error creating appointment: {str(e)}")
                return render(request, "main/appointment.html", {"form": form})
        else:
            # Form is not valid, show errors
            return render(request, "main/appointment.html", {
                "form": form, 
                "calendar_data": json.dumps({})
            })
    else:
        # Display the empty form when the request is GET
        form = AppointmentForm()

        try:
            # Sync available slots from Zoom (could be done via background task)
            slots_created = sync_available_slots()
            logger.info(f"Synced Zoom slots: {slots_created} new slots created")
            
            # Get available slots for next 2 weeks
            start_date = timezone.now().date()
            end_date = start_date + datetime.timedelta(days=14)
            available_slots = get_available_slots(start_date=start_date, end_date=end_date)
            
            # Group slots by date for the calendar
            calendar_data = {}
            for slot in available_slots:
                date_str = slot.start_time.strftime('%Y-%m-%d')
                if date_str not in calendar_data:
                    calendar_data[date_str] = []
                
                calendar_data[date_str].append({
                    'id': slot.id,
                    'start': slot.start_time.strftime('%H:%M'),
                    'end': slot.end_time.strftime('%H:%M'),
                    'formatted': slot.start_time.strftime('%I:%M %p')
                })
                
            logger.info(f"Found {len(available_slots)} available Zoom slots")
        except Exception as e:
            logger.error(f"Error syncing Zoom slots: {str(e)}")
            calendar_data = {}

    # Convert calendar_data to JSON with proper error handling
    try:
        calendar_data_json = json.dumps(calendar_data)
    except Exception as e:
        logger.error(f"Error converting calendar data to JSON: {str(e)}")
        calendar_data_json = json.dumps({})

    # Render the appointment page with the form and calendar data
    context = {
        "form": form,
        "calendar_data": calendar_data_json
    }
    
    # Only add success flag if this is not a form validation error
    if 'success' in locals():
        context["success"] = success
    
    return render(request, "main/appointment.html", context)

# Add an API endpoint to get slots for a specific date range
def get_zoom_slots(request):
    try:
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        
        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().date()
            
        if end_date_str:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = start_date + datetime.timedelta(days=14)
        
        available_slots = get_available_slots(start_date, end_date)
        
        # Format slots for JSON response
        slots_data = []
        for slot in available_slots:
            slots_data.append({
                'id': slot.id,
                'date': slot.start_time.strftime('%Y-%m-%d'),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
                'formatted': slot.start_time.strftime('%I:%M %p')
            })
        
        return JsonResponse({'success': True, 'slots': slots_data})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Endpoint to book a slot (for AJAX)
@require_POST
def book_zoom_slot(request):
    try:
        data = json.loads(request.body)
        slot_id = data.get('slot_id')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        notes = data.get('notes', '')
        
        success, result = book_appointment_slot(
            slot_id=slot_id,
            name=name,
            email=email,
            phone=phone,
            notes=notes
        )
        
        if success:
            return JsonResponse({
                'success': True, 
                'meeting': result
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def contact(request):
    # Fetch the BusinessContact object (you can modify this to your query)
    business_contact = BusinessContact.objects.all()  # Assuming there's only one or you want the first one
    
    # Get map URL from settings
    map_url = get_maps_settings()
    business_hours = get_business_hours()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            addressline2 = form.cleaned_data['addressline2']
            city = form.cleaned_data['city']
            zipcode =  form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            reason = form.cleaned_data['reason']

            # Prepare the email content
            subject = f"New Message from {name}"
            message = f"""
            You have received a new message from {name}.

            Phone: {phone}
            Email: {email}
            Address: {address}
            Address Line 2: {addressline2 if addressline2 else 'N/A'}
            City: {city}
            State: {state}
            Zipcode: {zipcode}
            Country: {country}

            Reason for contact:
            {reason}
            """

            from_email = email  # This is the user's email, but we're sending to your email

            # Get contact email from settings
            from main.settings_service import get_email_settings
            email_settings = get_email_settings()
            contact_email = email_settings['CONTACT_EMAIL']

            try:
                # Send the email to your email address (now from settings)
                send_mail(
                    subject,
                    message,
                    from_email,
                    [contact_email],  # Use contact email from settings
                    fail_silently=False,
                )

                # Save the data to the ContactUs model
                contactus = Contactus(
                    name=name,
                    phone=phone,
                    email=email,
                    address=address,
                    addressline2=addressline2,
                    city=city,
                    zipcode=zipcode,
                    state=state,
                    country=country,
                    reason=reason,
                    status='pending'
                )
                contactus.save()

                return render(request, "main/contact.html", {
                    "form": form, 
                    "success": True, 
                    "business_contact": business_contact,
                    "map_url": map_url,
                    "business_hours": business_hours
                })
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')
    else:
        # Display the empty form when the request is GET
        form = ContactForm()

    # Render the contact page with the form
    return render(request, "main/contact.html", {
        "form": form, 
        "business_contact": business_contact,
        "map_url": map_url,
        "business_hours": business_hours
    })

def services(request):
    services_section = ServicesSection.objects.all()
    return render(request, "main/services.html", {"services": services_section})

# Insurance Calculator View
def insurance_calculator(request):
    logger.debug("Insurance calculator view called")
    # Get all insurance types for display
    insurance_types = InsuranceType.objects.all()
    states = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia'
    }
    
    if request.method == "POST":
        logger.debug(f"POST data received: {request.POST}")
        
        # Get the insurance type ID from the POST data
        insurance_type_id = request.POST.get('insurance_type')
        
        if not insurance_type_id:
            return render(request, "main/insurance_calculator.html", {
                "insurance_types": insurance_types,
                "states": states,
                "error": "Please select an insurance type."
            })
        
        try:
            # Get the insurance type object
            insurance_type = InsuranceType.objects.get(id=insurance_type_id)
            insurance_type_name = insurance_type.name.lower()
            
            # Get coverage amount and term based on insurance type
            coverage_amount_field = f"{insurance_type_name}_coverage_amount"
            term_years_field = f"{insurance_type_name}_term_years"
            
            coverage_amount = request.POST.get(coverage_amount_field)
            term_years = request.POST.get(term_years_field)
            
            if not coverage_amount or not term_years:
                return render(request, "main/insurance_calculator.html", {
                    "insurance_types": insurance_types,
                    "states": states, 
                    "error": "Please provide both coverage amount and term years."
                })
            
            # Get basic info
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            state = request.POST.get('state')
            
            if not age or not gender:
                return render(request, "main/insurance_calculator.html", {
                    "insurance_types": insurance_types, 
                    "states": states,
                    "error": "Please enter your age and gender."
                })
            
            try:
                age = int(age)
                coverage_amount = Decimal(coverage_amount)
                term_years = Decimal(term_years)
            except (ValueError, decimal.InvalidOperation) as e:
                logger.error(f"Error converting values: {str(e)}")
                return render(request, "main/insurance_calculator.html", {
                    "insurance_types": insurance_types, 
                    "states": states,
                    "error": "Please enter valid numeric values."
                })
            
            # Get the state name if state is provided
            state_name = states.get(state) if state else None
            
            # Get the base rate for the insurance type, age, gender
            
            # Find the base rate
            try:
                base_rate = InsuranceBaseRate.objects.get(
                    insurance_type=insurance_type,
                    min_age__lte=age,
                    max_age__gte=age,
                    gender=gender
                )
                logger.debug(f"Found exact gender match rate for {insurance_type.name}, age {age}, gender {gender}")
            except InsuranceBaseRate.DoesNotExist:
                # Try with gender 'ANY' as fallback for gender-neutral pricing
                try:
                    base_rate = InsuranceBaseRate.objects.get(
                        insurance_type=insurance_type,
                        min_age__lte=age,
                        max_age__gte=age,
                        gender='ANY'
                    )
                    logger.debug(f"Using gender-neutral rate for {insurance_type.name}, age {age}")
                except InsuranceBaseRate.DoesNotExist:
                    logger.error(f"No base rate found for {insurance_type.name}, age {age}, gender {gender} or ANY")
                    return render(request, "main/insurance_calculator.html", {
                        "insurance_types": insurance_types, 
                        "states": states,
                        "error": f"Sorry, we couldn't calculate a premium for your profile. Please contact our agents for a personalized quote."
                    })
            
            logger.debug(f"Found base rate: {base_rate.base_monthly_rate} for {insurance_type.name}, age {age}, gender {gender}")
            
            # Calculate base premium
            monthly_premium = calculate_premium(
                base_rate=base_rate.base_monthly_rate,
                coverage_amount=coverage_amount,
                term_years=term_years,
                insurance_type=insurance_type,
                age=age,
                gender=gender,
                request_data=request.POST
            )
            
            # Apply state adjustments if a state is selected
            state_factor = 1.0
            state_factor_description = None
            state_factor_explanation = None
            state_regulation = None
            
            if state:
                try:
                    state_adjustment = StateRateAdjustment.objects.get(
                        insurance_type=insurance_type,
                        state=state
                    )
                    state_factor = state_adjustment.rate_multiplier
                    state_factor_description = state_adjustment.description
                    state_factor_explanation = None
                    
                    # Apply the state adjustment
                    monthly_premium = monthly_premium * Decimal(state_factor)
                    
                    # Get any specific state regulations
                    try:
                        state_regulation = StateRegulation.objects.get(
                            insurance_type=insurance_type,
                            state=state
                        )
                    except StateRegulation.DoesNotExist:
                        state_regulation = None
                        
                except StateRateAdjustment.DoesNotExist:
                    # No adjustment for this state, use default
                    pass
            
            # Generate the result
            annual_premium = (monthly_premium * 12) * Decimal('0.95')  # 5% discount for annual payment
            
            # Collect premium adjustment factors
            premium_adjustments = []
            
            # Get risk factors and their values
            factor_type_map = {
                'life': 'LIFE',
                'health': 'HEALTH',
                'auto': 'AUTO',
                'home': 'HOME'
            }
            factor_type = factor_type_map.get(insurance_type.name.lower(), 'LIFE')
            risk_factors = InsuranceRiskFactor.objects.filter(factor_type=factor_type)
            
            # Apply risk factors that are present in the request
            for factor in risk_factors:
                field_name = factor.name.lower().replace(' ', '_')  # Convert factor name to form field name format
                if field_name in request.POST:
                    value = request.POST.get(field_name)
                    try:
                        risk_value = RiskFactorValue.objects.get(
                            risk_factor=factor,
                            value_name=value
                        )
                        if risk_value.multiplier != 1.0:
                            premium_adjustments.append({
                                'name': factor.name,
                                'factor': f"{risk_value.multiplier:.2f}x",
                                'description': risk_value.description
                            })
                    except RiskFactorValue.DoesNotExist:
                        continue
            
            # Add state adjustment if applicable
            if state_factor != 1.0:
                premium_adjustments.append({
                    'name': 'State Adjustment',
                    'factor': f"{state_factor:.2f}x",
                    'description': f"Adjustment for {state_name} regulations"
                })
            
            # Get investment returns data for applicable insurance types
            investment_data = None
            if insurance_type.name.lower() in ['life', 'health'] and term_years >= 5:
                try:
                    investment_return = InsuranceInvestmentReturn.objects.get(
                        insurance_type=insurance_type,
                        term_years=term_years
                    )
                    
                    total_investment = annual_premium * term_years
                    
                    # Calculate maturity value
                    maturity_value = calculate_maturity_value(
                        premium=annual_premium,
                        years=term_years,
                        annual_return_rate=investment_return.annual_return_rate
                    )
                    
                    total_returns = maturity_value - total_investment
                    
                    if total_investment > 0:
                        return_percentage = (total_returns / total_investment) * 100
                    else:
                        return_percentage = 0
                        
                    # Generate conservative and aggressive scenarios
                    scenarios = {}
                    
                    if investment_return.conservative_return_rate:
                        conservative_maturity = calculate_maturity_value(
                            premium=annual_premium,
                            years=term_years,
                            annual_return_rate=investment_return.conservative_return_rate
                        )
                        conservative_returns = conservative_maturity - total_investment
                        scenarios['conservative'] = {
                            'rate': investment_return.conservative_return_rate,
                            'maturity_value': "{:,.2f}".format(conservative_maturity),
                            'total_returns': "{:,.2f}".format(conservative_returns)
                        }
                    
                    if investment_return.aggressive_return_rate:
                        aggressive_maturity = calculate_maturity_value(
                            premium=annual_premium,
                            years=term_years,
                            annual_return_rate=investment_return.aggressive_return_rate
                        )
                        aggressive_returns = aggressive_maturity - total_investment
                        scenarios['aggressive'] = {
                            'rate': investment_return.aggressive_return_rate,
                            'maturity_value': "{:,.2f}".format(aggressive_maturity),
                            'total_returns': "{:,.2f}".format(aggressive_returns)
                        }
                    
                    # Calculate effective annual yield
                    if total_investment > 0 and term_years > 0:
                        effective_annual_yield = ((maturity_value / total_investment) ** (1 / term_years)) - 1
                        effective_annual_yield = effective_annual_yield * 100  # Convert to percentage
                    else:
                        effective_annual_yield = 0
                    
                    investment_data = {
                        'total_investment': "{:,.2f}".format(total_investment),
                        'maturity_value': "{:,.2f}".format(maturity_value),
                        'total_returns': "{:,.2f}".format(total_returns),
                        'return_percentage': "{:.2f}".format(return_percentage),
                        'annual_return_rate': investment_return.annual_return_rate,
                        'term_years': term_years,
                        'tax_benefits': investment_return.tax_benefits,
                        'guaranteed_return': investment_return.guaranteed_return,
                        'maturity_bonus_percent': investment_return.maturity_bonus_percent,
                        'historical_performance': investment_return.historical_performance,
                        'effective_annual_yield': "{:.2f}".format(effective_annual_yield),
                        'scenarios': scenarios
                    }
                    
                except InsuranceInvestmentReturn.DoesNotExist:
                    # No investment return data for this type and term
                    pass
            
            # Get disclaimer text
            disclaimer_general = None
            disclaimer_specific = None
            
            try:
                # Get active disclaimer texts and use the first one if multiple exist
                disclaimer = DisclaimerText.objects.filter(
                    insurance_type=insurance_type,
                    is_active=True
                ).first()
                
                if disclaimer:
                    disclaimer_general = disclaimer.content
                    disclaimer_specific = disclaimer.title
            except Exception as e:
                logger.error(f"Error fetching disclaimer: {str(e)}")
                # No disclaimer for this insurance type
            
            result = {
                'monthly_premium': "{:.2f}".format(monthly_premium),
                'annual_premium': "{:.2f}".format(annual_premium),
                'coverage_amount': "{:,}".format(int(coverage_amount)),
                'term_years': term_years,
                'insurance_type': insurance_type.name,
                'state_name': state_name,
                'selected_state': state,
                'state_factor_description': state_factor_description,
                'state_factor_explanation': state_factor_explanation,
                'premium_adjustments': premium_adjustments,
                'investment_data': investment_data,
                'disclaimer_general': disclaimer_general,
                'disclaimer_specific': disclaimer_specific,
                'state_regulation': state_regulation
            }
            
            return render(request, "main/insurance_calculator.html", {
                "insurance_types": insurance_types,
                "states": states,
                "result": result
            })
            
        except InsuranceType.DoesNotExist:
            return render(request, "main/insurance_calculator.html", {
                "insurance_types": insurance_types,
                "states": states,
                "error": "Invalid insurance type selected."
            })
        except Exception as e:
            logger.error(f"Error calculating premium: {str(e)}", exc_info=True)
            return render(request, "main/insurance_calculator.html", {
                "insurance_types": insurance_types,
                "states": states,
                "error": f"An error occurred: {str(e)}"
            })
    
    # GET request
    return render(request, "main/insurance_calculator.html", {
        "insurance_types": insurance_types,
        "states": states
    })

