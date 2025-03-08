from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from main.forms import ContactForm, AppointmentForm
from main.models import Videos, HomeInfoSection, HomeSliderImage, Team, ServicesSection, BusinessContact, Contactus, Appointment, VideoDirect


# Create your views here.


def home(request):
    info_sections = HomeInfoSection.objects.all()
    slider_images = HomeSliderImage.objects.all()
    context = {
        'info_sections': info_sections,
        'slider_images': slider_images,
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
            appointment = form.cleaned_data['appointment']

            # Prepare the email content
            subject = f"New Appointment request - {name}"
            message = f"""
                You have received a new appointment request from {name} for date {appointment}. 

                Phone: {phone}
                Email: {email}
                Address: {address}
                Addressline2: {addressline2 if addressline2 else 'N/A'}
                City: {city}
                Zipcode: {zipcode}
                State: {state}
                Country: {country}

                Date of appointment:
                {appointment}
                """

            from_email = email  # This is the user's email, but we're sending to your email

            try:
                # Send the email to your email address (configured in settings.py)
                send_mail(
                    subject,
                    message,
                    from_email,
                    ["krishna.dhakal03@gmail.com"],  # Your email address where you want the messages sent
                    fail_silently=False,
                )

                # Save the data to the ContactUs model (adjust fields as needed)
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
                    appointment=appointment,
                    status='request'
                )
                appointment.save()

                return render(request, "main/appointment.html",
                              {"form": form, "success": True})
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')
    else:
        # Display the empty form when the request is GET
        form = AppointmentForm()

    # Render the contact page with the form
    return render(request, "main/appointment.html", {"form": form})


def contact(request):
    # Fetch the BusinessContact object (you can modify this to your query)
    business_contact = BusinessContact.objects.all()  # Assuming there's only one or you want the first one

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

            Reason for contact:
            {reason}
            """

            from_email = email  # This is the user's email, but we're sending to your email

            try:
                # Send the email to your email address (configured in settings.py)
                send_mail(
                    subject,
                    message,
                    from_email,
                    ["krishna.dhakal03@gmail.com"],  # Your email address where you want the messages sent
                    fail_silently=False,
                )

                # Save the data to the ContactUs model (adjust fields as needed)
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

                return render(request, "main/contact.html", {"form": form, "success": True, "business_contact": business_contact},)
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')
    else:
        # Display the empty form when the request is GET
        form = ContactForm()

    # Render the contact page with the form
    return render(request, "main/contact.html", {"form": form, "business_contact": business_contact })

def services(request):
    services_section = ServicesSection.objects.all()
    return render(request, "main/services.html", {"services": services_section})

