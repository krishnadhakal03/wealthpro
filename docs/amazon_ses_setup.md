# Amazon SES Email Setup Guide

This guide will walk you through setting up Amazon Simple Email Service (SES) with your WealthPro application. Amazon SES provides a reliable and cost-effective way to send transactional emails from your application.

## Prerequisites

1. An AWS account with appropriate permissions
2. A domain that you own and can modify DNS records for
3. WealthPro application with the latest database schema (including email settings fields)

## Step 1: Verify Your Domain in Amazon SES

1. Log in to the [AWS Management Console](https://aws.amazon.com/console/)
2. Navigate to the SES service
3. Select "Domains" from the left sidebar
4. Click "Verify a New Domain"
5. Enter your domain name and check "Generate DKIM Settings"
6. Click "Verify This Domain"
7. AWS will provide you with a set of DNS records (TXT and CNAME)
8. Add these records to your domain's DNS configuration through your domain registrar
9. Wait for verification to complete (this can take up to 72 hours, but usually happens within an hour)

## Step 2: Verify Email Addresses

While in the production environment you'll be able to send emails to any address once your domain is verified and you're out of the SES sandbox, during testing you'll need to verify individual email addresses:

1. In the SES console, select "Email Addresses" from the left sidebar
2. Click "Verify a New Email Address"
3. Enter the email address you want to use as your sender address (e.g., `info@yourdomain.com`)
4. Also verify any email addresses you'll use for testing recipients
5. Check your email and click the verification link in the AWS email

## Step 3: Create SMTP Credentials

1. In the SES console, select "SMTP Settings" from the left sidebar
2. Click "Create My SMTP Credentials"
3. Enter a name for your IAM user (e.g., "wealthpro-ses-smtp")
4. Click "Create"
5. Download the credentials CSV file containing your SMTP username and password
6. **Important**: This is the only time you'll be able to download these credentials, so store them securely

## Step 4: Configure WealthPro to Use Amazon SES

1. Log in to your WealthPro admin interface at `https://yoursite.com/admin/`
2. Navigate to "Main" > "Site Settings"
3. Locate the Email Settings section
4. Update the following fields:
   - **Email Provider**: Select "Amazon SES"
   - **Email Host**: Enter the SES SMTP endpoint for your region (e.g., `email-smtp.us-east-1.amazonaws.com`)
   - **Email Port**: Enter `587` (for TLS) or `465` (for SSL)
   - **Email Use TLS**: Check this if using port 587
   - **Email Use SSL**: Check this if using port 465 (do not enable both TLS and SSL)
   - **Email Host User**: Enter the SMTP username from your credentials
   - **Email Host Password**: Enter the SMTP password from your credentials
   - **Default From Email**: Enter your verified email address (e.g., `info@yourdomain.com`)
   - **Contact Email**: Enter the email where you want to receive form submissions
   - **AWS Region**: Select the AWS region where you set up SES

5. Click "Save" to apply the settings

## Step 5: Test Your Email Configuration

1. Return to the WealthPro home page
2. Navigate to the Contact page
3. Fill out the contact form with a verified email address (for testing)
4. Submit the form
5. Check that you receive the email at your designated contact email
6. Also verify that the sender receives a confirmation email

## Step 6: Request Production Access (Optional)

By default, AWS puts new SES accounts in the "sandbox" mode, which limits you to:
- Sending to verified email addresses only
- A maximum of 200 emails per 24-hour period
- A maximum send rate of 1 email per second

To move out of the sandbox:

1. In the SES console, select "Sending Statistics" from the left sidebar
2. Click "Request a Sending Limit Increase"
3. Fill out the request form with details about:
   - Your use case (e.g., transactional emails for financial services)
   - How you handle bounces and complaints
   - Your expected sending volume
4. Submit the request and wait for AWS to respond (typically within 24-48 hours)

## Troubleshooting

### Emails Not Sending

1. Check that your domain and email addresses are verified
2. Verify SMTP credentials are entered correctly
3. Ensure the correct port and TLS/SSL settings are used
4. Check AWS SES console for bounces or complaints
5. Look for any sending quota limitations

### Security Best Practices

1. Use IAM roles with restricted permissions for EC2 instances
2. Rotate SMTP credentials periodically
3. Enable logging for email sending activities
4. Monitor your sending reputation in the SES dashboard

## AWS SES Regional Endpoints

| Region | SMTP Endpoint |
|--------|---------------|
| US East (N. Virginia) | email-smtp.us-east-1.amazonaws.com |
| US East (Ohio) | email-smtp.us-east-2.amazonaws.com |
| US West (Oregon) | email-smtp.us-west-2.amazonaws.com |
| Asia Pacific (Mumbai) | email-smtp.ap-south-1.amazonaws.com |
| Asia Pacific (Sydney) | email-smtp.ap-southeast-2.amazonaws.com |
| Asia Pacific (Tokyo) | email-smtp.ap-northeast-1.amazonaws.com |
| Canada (Central) | email-smtp.ca-central-1.amazonaws.com |
| Europe (Frankfurt) | email-smtp.eu-central-1.amazonaws.com |
| Europe (Ireland) | email-smtp.eu-west-1.amazonaws.com |
| Europe (London) | email-smtp.eu-west-2.amazonaws.com |
| South America (São Paulo) | email-smtp.sa-east-1.amazonaws.com |

Choose the endpoint closest to your application servers or target audience for optimal delivery speed.

## Additional Resources

- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/Welcome.html)
- [Amazon SES SMTP Interface](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-smtp.html)
- [Moving Out of the Amazon SES Sandbox](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html) 