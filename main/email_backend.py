"""
Custom Django email backend that uses Amazon SES when possible,
and falls back to regular SMTP when needed.
"""
import logging
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from .ses_utils import send_email_ses

logger = logging.getLogger(__name__)

class SESEmailBackend:
    """
    Email backend that sends emails through Amazon SES using boto3.
    Falls back to SMTP if any issues occur.
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently
        self.smtp_backend = SMTPBackend(fail_silently=fail_silently, **kwargs)
        
    def send_messages(self, email_messages):
        """
        Send email messages using Amazon SES, with SMTP as fallback.
        
        Args:
            email_messages: List of django.core.mail.EmailMessage instances
            
        Returns:
            int: Number of successfully sent messages
        """
        if not email_messages:
            return 0
            
        # Try AWS SES first
        count = 0
        for message in email_messages:
            try:
                # Extract data from the EmailMessage object
                subject = message.subject
                body = message.body
                from_email = message.from_email
                to_emails = message.to
                
                # Check for HTML alternative
                html_body = None
                if message.content_subtype == 'html':
                    html_body = body
                    body = self._strip_html(body)  # Simple text version
                else:
                    # Check if there's an HTML alternative
                    for alt_content, alt_mimetype in getattr(message, 'alternatives', []):
                        if alt_mimetype == 'text/html':
                            html_body = alt_content
                            break
                
                # Send via SES
                success, result = send_email_ses(
                    subject=subject,
                    message=body,
                    recipient_email=to_emails,
                    sender=from_email,
                    html_message=html_body
                )
                
                if success:
                    count += 1
                else:
                    logger.warning(f"SES email failed: {result}. Falling back to SMTP.")
                    # Fall back to SMTP for this message
                    self.smtp_backend.send_messages([message])
                    count += 1
                    
            except Exception as e:
                logger.error(f"Error sending SES email: {str(e)}")
                if not self.fail_silently:
                    raise
                # Try SMTP as fallback if SES fails
                try:
                    self.smtp_backend.send_messages([message])
                    count += 1
                except Exception as smtp_e:
                    logger.error(f"Fallback SMTP also failed: {str(smtp_e)}")
                    if not self.fail_silently:
                        raise
                        
        return count
    
    def _strip_html(self, html_content):
        """Simple method to get plain text from HTML content"""
        import re
        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', html_content)
        # Replace multiple spaces and newlines
        text = re.sub(r'\s+', ' ', text)
        return text
        
    def close(self):
        """Close the connection to the email server"""
        self.smtp_backend.close() 