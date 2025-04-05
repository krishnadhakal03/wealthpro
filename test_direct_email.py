#!/usr/bin/env python
import os
import django
import sys
from datetime import datetime

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wealthpro.settings")
django.setup()

# After Django setup, import email modules
from django.core.mail import send_mail
from django.conf import settings

# Test recipient email - change this to your email address
TEST_EMAIL = "your-email@example.com"  # Replace with your real email

def test_direct_email():
    """Test sending a direct email"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"Sending test email at {timestamp}")
    print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
    print(f"TO: {TEST_EMAIL}")
    
    try:
        send_mail(
            subject=f"Test Email at {timestamp}",
            message="This is a test email sent directly using Django's send_mail function.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[TEST_EMAIL],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

if __name__ == "__main__":
    # Check if recipient email was provided as command line argument
    if len(sys.argv) > 1:
        TEST_EMAIL = sys.argv[1]
    
    print("\n" + "=" * 50)
    print("EMAIL CONFIGURATION")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"USE_SES: {getattr(settings, 'USE_SES', False)}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER[:5]}..." if settings.EMAIL_HOST_USER else "Not set")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 50 + "\n")
    
    test_direct_email()
    
    print("\nCheck your inbox for the test email.")
    print("If you don't see it, check your spam folder or email settings.") 