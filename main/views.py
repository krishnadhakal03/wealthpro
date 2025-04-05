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
    StateRateAdjustment
)
from .zoom_utils import (
    sync_available_slots, get_available_slots, 
    book_appointment_slot, create_zoom_meeting, mark_slot_unavailable
)
from main.settings_service import get_maps_settings, get_business_hours

# Create your views here.

logger = logging.getLogger(__name__)

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
    insurance_types = InsuranceType.objects.all()
    
    # Get all states for the dropdown
    states = dict(StateRateAdjustment.STATE_CHOICES)
    
    # Default empty context
    context = {
        'insurance_types': insurance_types,
        'states': states,
        'result': None,
    }
    
    if request.method == 'POST':
        # Check if this is a resubmission (browser refresh)
        current_timestamp = request.POST.get('timestamp', '0')
        session_timestamp = request.session.get('calculator_timestamp', '-1')  # Default to different value
        
        # Only treat as refresh if timestamps match exactly and are not empty
        if current_timestamp and session_timestamp and current_timestamp == session_timestamp:
            # This is a refresh, return the page without processing
            return render(request, "main/insurance_calculator.html", context)
        
        # Store timestamp in session to check for refreshes
        request.session['calculator_timestamp'] = current_timestamp
        
        # Extract form data
        insurance_type_id = request.POST.get('insurance_type')
        age = int(request.POST.get('age', 0))
        gender = request.POST.get('gender', 'ANY')
        coverage_amount = Decimal(request.POST.get('coverage_amount', 0))
        term_years = int(request.POST.get('term_years', 10))
        selected_state = request.POST.get('state', '')
        
        # Additional inputs based on insurance type
        vehicle_value = request.POST.get('vehicle_value', 0)
        home_value = request.POST.get('home_value', 0)
        health_condition = request.POST.get('health_condition', 'None')
        
        try:
            # Get insurance type
            insurance_type = InsuranceType.objects.get(id=insurance_type_id)
            
            # Find applicable base rate
            base_rate = InsuranceBaseRate.objects.filter(
                insurance_type=insurance_type,
                min_age__lte=age,
                max_age__gte=age
            ).filter(
                models.Q(gender=gender) | models.Q(gender='ANY')
            ).first()
            
            if base_rate:
                # Calculate premium - convert to Decimal to avoid type mismatch
                monthly_premium = base_rate.base_monthly_rate + (coverage_amount / Decimal('1000') * base_rate.rate_per_thousand)
                
                # Apply CSO mortality adjustment for life insurance
                if insurance_type.name.lower() == 'life':
                    # Apply 2017 CSO Mortality Table adjustment (simplified implementation)
                    # In a production environment, would load actual tables from a database
                    if age < 30:
                        mortality_factor = Decimal('0.95')  # Lower mortality risk for younger people
                    elif age < 50:
                        mortality_factor = Decimal('1.0')   # Baseline
                    elif age < 65:
                        mortality_factor = Decimal('1.15')  # Higher risk 
                    else:
                        mortality_factor = Decimal('1.35')  # Much higher risk for seniors
                    
                    # Apply gender-specific mortality adjustment based on CSO tables
                    if gender == 'F':
                        mortality_factor *= Decimal('0.9')  # Women generally have lower mortality rates
                    
                    monthly_premium *= mortality_factor
                
                # Apply adjustments based on insurance type and additional inputs
                if insurance_type.name.lower() == 'auto':
                    vehicle_value = Decimal(vehicle_value)
                    if vehicle_value > Decimal('50000'):
                        monthly_premium *= Decimal('1.2')  # 20% increase for luxury vehicles
                
                elif insurance_type.name.lower() == 'home':
                    home_value = Decimal(home_value)
                    if home_value > Decimal('500000'):
                        monthly_premium *= Decimal('1.15')  # 15% increase for high-value homes
                
                elif insurance_type.name.lower() == 'health':
                    if health_condition.lower() != 'none':
                        monthly_premium *= Decimal('1.3')  # 30% increase for pre-existing conditions
                
                # Apply state-specific adjustment if a state was selected
                if selected_state:
                    state_adjustment = StateRateAdjustment.objects.filter(
                        insurance_type=insurance_type,
                        state=selected_state
                    ).first()
                    
                    if state_adjustment:
                        monthly_premium *= state_adjustment.rate_multiplier
                        state_factor_description = f"{state_adjustment.get_state_display()} adjustment: {state_adjustment.rate_multiplier}x"
                        state_factor_explanation = state_adjustment.description or "State-specific regulatory adjustment"
                    else:
                        state_factor_description = None
                        state_factor_explanation = None
                
                annual_premium = monthly_premium * Decimal('12')
                
                # Calculate maturity and returns
                investment_data = None
                maturity_value = None
                total_investment = None
                total_returns = None
                annual_return_rate = None
                
                # Find investment return data for this insurance type and term
                investment_return = InsuranceInvestmentReturn.objects.filter(
                    insurance_type=insurance_type,
                    term_years=term_years
                ).first()
                
                # If no exact match for term, get the closest available term
                if not investment_return:
                    investment_return = InsuranceInvestmentReturn.objects.filter(
                        insurance_type=insurance_type
                    ).order_by(models.F('term_years') - term_years)[:1].first()
                
                if investment_return:
                    # Calculate investment returns and maturity value
                    total_investment = annual_premium * Decimal(str(investment_return.term_years))
                    annual_return_rate = investment_return.annual_return_rate
                    
                    # Improved compound interest calculation using Time Value of Money formula
                    # FV = P(1+r)^n where P=principal, r=rate, n=time period
                    rate = annual_return_rate / Decimal('100')
                    maturity_value = total_investment * (Decimal('1') + rate) ** Decimal(str(investment_return.term_years))
                    
                    # Add maturity bonus if applicable
                    if investment_return.maturity_bonus_percent > 0:
                        bonus = total_investment * (investment_return.maturity_bonus_percent / Decimal('100'))
                        maturity_value += bonus
                    
                    total_returns = maturity_value - total_investment
                    
                    # Calculate NAIC Model Rule compliant annual effective yield
                    effective_annual_yield = ((maturity_value / total_investment) ** (Decimal('1') / Decimal(str(investment_return.term_years)))) - Decimal('1')
                    effective_annual_yield_percent = effective_annual_yield * Decimal('100')
                    
                    investment_data = {
                        'term_years': investment_return.term_years,
                        'annual_return_rate': float(annual_return_rate),
                        'guaranteed_return': investment_return.guaranteed_return,
                        'tax_benefits': investment_return.tax_benefits,
                        'maturity_bonus_percent': float(investment_return.maturity_bonus_percent),
                        'total_investment': round(float(total_investment), 2),
                        'maturity_value': round(float(maturity_value), 2),
                        'total_returns': round(float(total_returns), 2),
                        'return_percentage': round(float(total_returns / total_investment * 100), 2) if total_investment else 0,
                        'effective_annual_yield': round(float(effective_annual_yield_percent), 2),
                    }
                
                # Store results
                result = {
                    'insurance_type': insurance_type.name,
                    'monthly_premium': round(float(monthly_premium), 2),
                    'annual_premium': round(float(annual_premium), 2),
                    'coverage_amount': float(coverage_amount),
                    'term_years': term_years,
                    'selected_state': selected_state,
                    'state_name': states.get(selected_state, ''),
                    'state_factor_description': state_factor_description if selected_state else None,
                    'state_factor_explanation': state_factor_explanation if selected_state else None,
                    'investment_data': investment_data
                }
                
                context['result'] = result
            else:
                context['error'] = "No applicable insurance rate found for your criteria."
        
        except Exception as e:
            logger.error(f"Error calculating insurance premium: {str(e)}")
            context['error'] = "An error occurred while calculating your insurance premium."
    
    return render(request, "main/insurance_calculator.html", context)

