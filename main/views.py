from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from main.forms import ContactForm
from main.models import Videos, HomeInfoSection, HomeSliderImage, Team, ServicesSection


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
    return render(request, "main/videos.html", {"vid": vid})

def appointment(request):
    return render(request, "main/appointment.html", {})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
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
                return render(request, "main/contact.html", {"form": form, "success": True})
            except Exception as e:
                return HttpResponse(f'Error: {str(e)}')
    else:
        # Display the empty form when the request is GET
        form = ContactForm()

    # Render the contact page with the form
    return render(request, "main/contact.html", {"form": form})

def services(request):
    services_section = ServicesSection.objects.all()
    return render(request, "main/services.html", {"services": services_section})

