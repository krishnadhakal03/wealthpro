"""
Django management command to set up and verify AWS SES email addresses.
"""
import sys
from django.core.management.base import BaseCommand
from django.conf import settings
from main.ses_utils import verify_email_identity, get_verified_identities

class Command(BaseCommand):
    help = "Set up and verify email addresses for Amazon SES"

    def add_arguments(self, parser):
        parser.add_argument(
            '--verify',
            metavar='EMAIL',
            help='Verify an email address with SES',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all verified email addresses',
        )

    def handle(self, *args, **options):
        if not self.check_aws_credentials():
            self.stderr.write(self.style.ERROR(
                "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
            ))
            sys.exit(1)
            
        if options['verify']:
            email = options['verify']
            self.stdout.write(self.style.WARNING(f"Requesting verification for: {email}"))
            success, message = verify_email_identity(email)
            
            if success:
                self.stdout.write(self.style.SUCCESS(message))
                self.stdout.write(self.style.WARNING(
                    "Please check the email inbox and follow the verification link from AWS."
                ))
            else:
                self.stderr.write(self.style.ERROR(f"Verification request failed: {message}"))
                
        elif options['list']:
            self.list_verified_identities()
            
        else:
            self.stdout.write(self.style.WARNING(
                "No action specified. Use --verify EMAIL to verify an email address or --list to list verified addresses."
            ))
            
    def check_aws_credentials(self):
        """Check if AWS credentials are available in environment"""
        import os
        return os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_SECRET_ACCESS_KEY')
        
    def list_verified_identities(self):
        """List all verified email addresses"""
        identities = get_verified_identities()
        
        if not identities:
            self.stdout.write(self.style.WARNING("No verified email addresses found."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Found {len(identities)} verified email identities:"))
        for identity in identities:
            self.stdout.write(f"  - {identity}")
        
        # Check if the DEFAULT_FROM_EMAIL is verified
        from_email = settings.DEFAULT_FROM_EMAIL
        if from_email in identities:
            self.stdout.write(self.style.SUCCESS(f"✓ DEFAULT_FROM_EMAIL ({from_email}) is verified."))
        else:
            self.stdout.write(self.style.ERROR(
                f"✗ DEFAULT_FROM_EMAIL ({from_email}) is NOT verified. Emails won't be sent until verified."
            ))
            self.stdout.write(self.style.WARNING(
                f"Run 'python manage.py setup_ses --verify {from_email}' to request verification."
            )) 