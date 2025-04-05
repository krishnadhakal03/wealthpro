#!/usr/bin/env python
import os
import django
import sys
import json
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wealthpro.settings")
django.setup()

# After Django setup, import required modules
from django.core.mail import send_mail
from django.conf import settings
from django.test import Client, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

# Set allowed hosts for testing
from django.conf import settings
settings.ALLOWED_HOSTS += ['testserver']

def test_direct_email():
    """Test sending email directly using Django's send_mail"""
    print("\n🧪 Testing direct email sending...")
    print(f"Using DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Using CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    
    try:
        send_mail(
            subject="Direct Test Email",
            message="This is a test email sent directly via Django's send_mail function.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        print("✅ Direct email test SUCCESS")
    except Exception as e:
        print(f"❌ Direct email test FAILED: {str(e)}")

def test_contact_form():
    """Test the contact form submission"""
    print("\n🧪 Testing contact form submission...")
    
    client = Client()
    
    # Contact form data
    form_data = {
        'name': 'Test User',
        'phone': '555-123-4567',
        'email': 'testuser@example.com',
        'address': '123 Test Street',
        'addressline2': 'Apt 456',
        'city': 'Test City',
        'zipcode': '12345',
        'state': 'TS',
        'country': 'Test Country',
        'reason': 'This is a test submission from the automated testing script.'
    }
    
    try:
        # Submit the contact form
        response = client.post(reverse('contact'), form_data)
        
        if response.status_code == 200 and 'success' in str(response.content):
            print("✅ Contact form test SUCCESS")
            print("   Email should be sent TO: " + settings.CONTACT_EMAIL)
            print("   Email should be sent FROM: " + settings.DEFAULT_FROM_EMAIL)
        else:
            print(f"❌ Contact form test FAILED: Status code {response.status_code}")
            print(f"   Response: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Contact form test FAILED with exception: {str(e)}")

def test_appointment_form():
    """Test the appointment form submission"""
    print("\n🧪 Testing appointment form submission...")
    
    client = Client()
    
    # Appointment form data
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    
    form_data = {
        'name': 'Test Appointment User',
        'phone': '555-987-6543',
        'email': 'testappointment@example.com',
        'appointment': tomorrow_str,
        'address': '789 Appointment Street',
        'addressline2': 'Suite 101',
        'city': 'Appointment City',
        'zipcode': '54321',
        'state': 'AS',
        'country': 'Appointment Country',
    }
    
    try:
        # Submit the appointment form
        response = client.post(reverse('appointment'), form_data)
        
        if response.status_code == 200 and 'success' in str(response.content):
            print("✅ Appointment form test SUCCESS")
            print("   Appointment confirmation should be sent TO: " + settings.CONTACT_EMAIL)
            print("   Client notification should be sent TO: testappointment@example.com")
            print("   Both emails should be sent FROM: " + settings.DEFAULT_FROM_EMAIL)
        else:
            print(f"❌ Appointment form test FAILED: Status code {response.status_code}")
            print(f"   Response: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Appointment form test FAILED with exception: {str(e)}")

if __name__ == "__main__":
    print("=" * 70)
    print(f"TESTING EMAIL CONFIGURATION")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER[:5]}...{settings.EMAIL_HOST_USER[-3:]}")
    print(f"AWS_REGION: {getattr(settings, 'AWS_REGION', 'not set')}")
    print(f"USE_SES: {getattr(settings, 'USE_SES', False)}")
    print("=" * 70)
    
    # Run the tests
    test_direct_email()
    test_contact_form()
    test_appointment_form()
    
    print("\n" + "=" * 70)
    print("Tests completed. Check inbox of both:")
    print(f"1. {settings.CONTACT_EMAIL} - should receive contact form and appointment notifications")
    print(f"2. testappointment@example.com - would receive client confirmation (if it were real)")
    print("=" * 70) 