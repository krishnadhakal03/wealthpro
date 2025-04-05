#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wealthpro.settings")
django.setup()

# After Django setup, import SES utility
from main.ses_utils import verify_email_identity, get_verified_identities

# Domain email address to verify
EMAIL_TO_VERIFY = "legacy@nextgenerationwealthpro.com"

if __name__ == "__main__":
    # Override email if provided as command line argument
    if len(sys.argv) > 1:
        EMAIL_TO_VERIFY = sys.argv[1]
    
    print(f"Attempting to verify email: {EMAIL_TO_VERIFY}")
    
    # First check if already verified
    print("Checking existing verified identities...")
    identities = get_verified_identities()
    
    if EMAIL_TO_VERIFY in identities:
        print(f"✅ {EMAIL_TO_VERIFY} is already verified in SES!")
    else:
        print(f"{EMAIL_TO_VERIFY} is not yet verified. Requesting verification...")
        
        # Request verification
        success, message = verify_email_identity(EMAIL_TO_VERIFY)
        
        if success:
            print(f"✅ Verification email sent to {EMAIL_TO_VERIFY}")
            print("IMPORTANT: You must click the verification link in the email to complete verification")
            print("It may take a few minutes for the verification email to arrive")
        else:
            print(f"❌ Failed to request verification: {message}")
            
    print("\nCurrently verified identities in SES:")
    for identity in identities:
        print(f"  • {identity}") 