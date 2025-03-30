# Amazon SES Email Setup for WealthPro

This guide covers setting up Amazon SES (Simple Email Service) for sending emails in the WealthPro application.

## Prerequisites

1. An AWS account with access to SES
2. A domain you control for sending emails
3. AWS access keys with SES permissions

## Step 1: Create SMTP Credentials in AWS

1. Log in to your AWS Management Console
2. Navigate to the SES (Simple Email Service) dashboard
3. Click on "SMTP Settings" in the left menu
4. Click "Create SMTP Credentials"
5. Note: these credentials are different from your regular AWS access keys
6. Save the SMTP Username and Password securely - you'll need them for the application

## Step 2: Verify Email Addresses

In SES sandbox mode, you must verify both sender and recipient email addresses:

1. In the SES dashboard, click "Verified Identities"
2. Click "Create Identity"
3. Choose "Email address" and enter the address you want to verify
4. Click "Create Identity"
5. Check the inbox for a verification email and click the verification link

**Important:** At minimum, verify these email addresses:
- Your site's default sender email (e.g., info@nextgenerationwealthpro.com)
- Your contact email where form submissions are sent

## Step 3: Configure the Application

Update your `.env` file with the following variables:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-2
EMAIL_HOST_USER=your_ses_smtp_username
EMAIL_HOST_PASSWORD=your_ses_smtp_password
USE_SES=True
```

Alternatively, directly update `settings.py`:

```python
# AWS SES configuration
AWS_REGION = 'us-east-2'
USE_SES = True
EMAIL_HOST_USER = 'your_ses_smtp_username'
EMAIL_HOST_PASSWORD = 'your_ses_smtp_password'
```

## Step 4: Verify Configuration

Use the management command to check your setup:

```bash
# List all verified identities
python manage.py setup_ses --list

# Request verification for a new email
python manage.py setup_ses --verify info@yourdomain.com
```

## Step 5: Moving Out of SES Sandbox

By default, new AWS accounts are in "SES Sandbox" mode, which has limitations:
- Can only send to verified email addresses
- Daily sending quota of 200 emails
- Maximum send rate of 1 email/second

To move out of sandbox mode:
1. Go to SES dashboard
2. Click "Account dashboard"
3. Under "Sending statistics", click "Request production access"
4. Fill out the request form with your email use case
5. Wait for AWS approval (typically 24-48 hours)

## Troubleshooting

### Emails not sending via SES

1. Check if all required AWS credentials are set
2. Verify both sender and recipient emails are verified (in sandbox mode)
3. Check Django logs for error messages
4. Ensure your AWS account has SES permissions

### SES quota or throttling issues

1. Check your current sending quotas in the SES dashboard
2. Request a quota increase if needed
3. Implement sending rate limits in your application

## Fall-back to SMTP

The application will automatically fall back to the SMTP configuration if:
- `USE_SES` is set to `False`
- SES credentials are not provided
- SES sending fails

This ensures your application will continue to send emails even if there are issues with SES.

## Additional Resources

- [AWS SES Documentation](https://docs.aws.amazon.com/ses/latest/dg/Welcome.html)
- [SES SMTP Interface](https://docs.aws.amazon.com/ses/latest/dg/send-email-smtp.html)
- [SES Production Access Guide](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html) 