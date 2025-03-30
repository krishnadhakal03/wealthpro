"""
AWS SES Utilities for Email Functionality
This module provides helper functions for sending emails via Amazon SES.
"""
import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)

def get_ses_client():
    """
    Create and return an AWS SES client configured with the AWS region.
    """
    # Use the region from settings, or default to us-east-2 (Ohio)
    aws_region = getattr(settings, 'AWS_REGION', 'us-east-2')
    
    # Create a new SES client
    client = boto3.client(
        'ses',
        region_name=aws_region,
        # AWS credentials are automatically picked up from environment variables:
        # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    )
    return client

def send_email_ses(subject, message, recipient_email, sender=None, html_message=None):
    """
    Send an email using Amazon SES.
    
    Args:
        subject (str): The email subject
        message (str): The plain text message body
        recipient_email (str or list): The recipient email address(es)
        sender (str, optional): Sender email address. If not provided, uses DEFAULT_FROM_EMAIL
        html_message (str, optional): HTML version of the message body
        
    Returns:
        bool: True if email was sent successfully, False otherwise
        str: Message ID if successful, error message if not
    """
    # Use the provided sender or fall back to the default
    sender_email = sender or settings.DEFAULT_FROM_EMAIL
    
    # Ensure recipient_email is a list
    if isinstance(recipient_email, str):
        recipient_email = [recipient_email]
        
    try:
        client = get_ses_client()
        
        # Prepare the email content
        email_message = {
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': message,
                    'Charset': 'UTF-8'
                }
            }
        }
        
        # Add HTML content if provided
        if html_message:
            email_message['Body']['Html'] = {
                'Data': html_message,
                'Charset': 'UTF-8'
            }
        
        # Send the email
        response = client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': recipient_email,
            },
            Message=email_message
        )
        
        logger.info(f"Email sent successfully to {', '.join(recipient_email)}. MessageId: {response['MessageId']}")
        return True, response['MessageId']
        
    except ClientError as e:
        error = e.response['Error']['Message']
        logger.error(f"Failed to send email to {', '.join(recipient_email)}: {error}")
        return False, error
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}")
        return False, str(e)

def verify_email_identity(email):
    """
    Request verification for an email address in SES.
    SES will send a verification email to the address.
    
    Args:
        email (str): The email address to verify
        
    Returns:
        bool: True if verification request was sent successfully
        str: Success or error message
    """
    try:
        client = get_ses_client()
        response = client.verify_email_identity(EmailAddress=email)
        logger.info(f"Verification email sent to {email}")
        return True, f"Verification email sent to {email}. Please check the inbox and follow the instructions."
    except ClientError as e:
        error = e.response['Error']['Message']
        logger.error(f"Failed to request verification for {email}: {error}")
        return False, error
    except Exception as e:
        logger.error(f"Unexpected error requesting verification: {str(e)}")
        return False, str(e)

def get_verified_identities():
    """
    List all verified email addresses and domains in SES.
    
    Returns:
        list: List of verified email addresses and domains
    """
    try:
        client = get_ses_client()
        response = client.list_identities(IdentityType='EmailAddress')
        return response.get('Identities', [])
    except ClientError as e:
        logger.error(f"Failed to list verified identities: {e.response['Error']['Message']}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error listing identities: {str(e)}")
        return [] 