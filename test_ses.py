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
from main.ses_utils import send_email_ses, get_verified_identities

# Test email recipient
TEST_EMAIL = "your-email@example.com"  # Replace with your email

def test_django_email():
    """Test sending email using Django's send_mail function"""
    print("Testing Django's send_mail...")
    
    try:
        send_mail(
            subject=f'SES Test from Django {datetime.now().strftime("%H:%M:%S")}',
            message='This is a test email sent using Django send_mail through AWS SES.',
            from_email=None,  # Will use DEFAULT_FROM_EMAIL from settings
            recipient_list=[TEST_EMAIL],
            fail_silently=False,
        )
        print("✅ Django send_mail SUCCESS")
    except Exception as e:
        print(f"❌ Django send_mail FAILED: {str(e)}")

def test_ses_direct():
    """Test sending email using the SES utility function directly"""
    print("\nTesting direct SES API...")
    
    try:
        success, result = send_email_ses(
            subject=f'SES Direct API Test {datetime.now().strftime("%H:%M:%S")}',
            message='This is a test email sent using boto3 SES client directly.',
            recipient_email=TEST_EMAIL,
            sender=None  # Will use DEFAULT_FROM_EMAIL from settings
        )
        
        if success:
            print(f"✅ Direct SES SUCCESS: {result}")
        else:
            print(f"❌ Direct SES FAILED: {result}")
    except Exception as e:
        print(f"❌ Direct SES FAILED with exception: {str(e)}")

def check_verified_identities():
    """Check which email addresses are verified in SES"""
    print("\nChecking verified identities in SES...")
    
    try:
        identities = get_verified_identities()
        if identities:
            print(f"✅ Found {len(identities)} verified identities:")
            for identity in identities:
                print(f"  • {identity}")
        else:
            print("⚠️ No verified identities found.")
    except Exception as e:
        print(f"❌ Failed to get verified identities: {str(e)}")

if __name__ == "__main__":
    # Update the test email if provided as argument
    if len(sys.argv) > 1:
        TEST_EMAIL = sys.argv[1]
    
    print(f"SES Test using recipient: {TEST_EMAIL}")
    print(f"DEFAULT_FROM_EMAIL: {django.conf.settings.DEFAULT_FROM_EMAIL}")
    print(f"EMAIL_HOST_USER: {django.conf.settings.EMAIL_HOST_USER[:5]}...{django.conf.settings.EMAIL_HOST_USER[-3:]}")
    print(f"Using SES: {getattr(django.conf.settings, 'USE_SES', False)}")
    print(f"AWS Region: {getattr(django.conf.settings, 'AWS_REGION', 'not set')}")
    print("=" * 50)
    
    # Run tests
    check_verified_identities()
    test_django_email()
    test_ses_direct()
    
    print("\nTests completed. Check your inbox for test emails.") 