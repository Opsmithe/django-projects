# Email Feature Documentation - Tennis Club Application

## Table of Contents
1. [Overview](#overview)
2. [Email Configuration](#email-configuration)
3. [Email Functions](#email-functions)
4. [Email Templates](#email-templates)
5. [Testing Emails](#testing-emails)
6. [Production Setup](#production-setup)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

---

## Overview

The Tennis Club application includes a comprehensive email system that automatically sends emails for:
- **Welcome emails** when new members register
- **Update notifications** when member information is changed
- **Deletion confirmations** when member accounts are removed
- **Bulk emails** for announcements (future feature)

### Email Flow Diagram

```
Member Registration
    ↓
Form Submitted
    ↓
Member Created in Database
    ↓
send_welcome_email() Called
    ↓
Email Template Rendered
    ↓
Email Sent (Console/SMTP)
    ↓
Success Message Displayed
```

---

## Email Configuration

### Development Configuration (Current)

Located in `project/settings.py`:

```python
# Email prints to console for testing
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'Tennis Club <noreply@tennisclub.com>'
EMAIL_TIMEOUT = 10
```

**How it works:**
- Emails are printed to the console/terminal
- No actual emails are sent
- Perfect for development and testing
- No external email service needed

### Production Configuration (Gmail Example)

For production, uncomment and configure in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # NOT your regular password!
DEFAULT_FROM_EMAIL = 'Tennis Club <your-email@gmail.com>'
```

**Important:** For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Generate an App Password (not your regular password)
3. Use the App Password in `EMAIL_HOST_PASSWORD`

### Other Email Providers

**SendGrid:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

**AWS SES:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-ses-smtp-username'
EMAIL_HOST_PASSWORD = 'your-ses-smtp-password'
```

**Mailgun:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@your-domain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

---

## Email Functions

All email functions are located in `club/emails.py`.

### 1. send_welcome_email(member)

**Purpose:** Send a welcome email to newly registered members.

**Parameters:**
- `member` (Names object): The newly created member

**Returns:**
- `bool`: True if email sent successfully, False otherwise

**Usage:**
```python
from club.emails import send_welcome_email
from club.models import Names

# After creating a member
member = Names.objects.create(
    firstname="John",
    lastname="Doe",
    email="john@example.com",
    # ... other fields
)

# Send welcome email
success = send_welcome_email(member)
if success:
    print("Welcome email sent!")
else:
    print("Failed to send email")
```

**Email Content:**
- Personalized greeting
- Member registration details
- Next steps and getting started guide
- Contact information
- Professional HTML template

**Example Output (Console):**
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome to Tennis Club, John!
From: Tennis Club <noreply@tennisclub.com>
To: john@example.com
Date: Thu, 26 Feb 2026 10:30:00 -0000

Dear John Doe,

Welcome to Tennis Club! Your registration has been successfully completed...
```

### 2. send_simple_welcome_email(member)

**Purpose:** Send a plain text welcome email (alternative to HTML version).

**Parameters:**
- `member` (Names object): The member to send email to

**Returns:**
- `bool`: True if successful, False otherwise

**Usage:**
```python
from club.emails import send_simple_welcome_email

# Send simple text email
send_simple_welcome_email(member)
```

**When to use:**
- Email clients that don't support HTML
- Simpler email requirements
- Faster email generation
- Fallback option

### 3. send_member_update_notification(member, updated_by=None)

**Purpose:** Notify member when their information is updated.

**Parameters:**
- `member` (Names object): The updated member
- `updated_by` (str, optional): Name of person who made the update

**Returns:**
- `bool`: True if successful, False otherwise

**Usage:**
```python
from club.emails import send_member_update_notification

# After updating member
member.city = "New York"
member.save()

# Send notification
send_member_update_notification(member, updated_by="Admin")
```

### 4. send_deletion_confirmation(member_email, member_name)

**Purpose:** Send confirmation when member account is deleted.

**Parameters:**
- `member_email` (str): Email address of deleted member
- `member_name` (str): Full name of deleted member

**Returns:**
- `bool`: True if successful, False otherwise

**Usage:**
```python
from club.emails import send_deletion_confirmation

# Before deleting member
member_email = member.email
member_name = f"{member.firstname} {member.lastname}"

# Send confirmation
send_deletion_confirmation(member_email, member_name)

# Then delete
member.delete()
```

### 5. send_bulk_email(subject, message, recipient_list)

**Purpose:** Send emails to multiple recipients (announcements, newsletters).

**Parameters:**
- `subject` (str): Email subject
- `message` (str): Email body
- `recipient_list` (list): List of email addresses

**Returns:**
- `int`: Number of emails sent successfully

**Usage:**
```python
from club.emails import send_bulk_email
from club.models import Names

# Get all member emails
members = Names.objects.all()
emails = [m.email for m in members]

# Send announcement
sent_count = send_bulk_email(
    subject="Important Club Announcement",
    message="Dear members, we have exciting news...",
    recipient_list=emails
)

print(f"Sent to {sent_count} members")
```

---

## Email Templates

### Template Location
```
club/templates/emails/
└── welcome_email.html
```

### Template Structure

**welcome_email.html** includes:
- Responsive HTML design
- Inline CSS for email client compatibility
- Professional branding
- Member information display
- Call-to-action buttons
- Footer with contact info

### Template Variables

Available in email templates:

```django
{{ member.firstname }}          # Member's first name
{{ member.lastname }}            # Member's last name
{{ member.email }}               # Member's email
{{ member.phoneNumber }}         # Member's phone
{{ member.city }}                # Member's city
{{ member.location }}            # Member's location
{{ member.date_joined }}         # Registration date
{{ club_name }}                  # "Tennis Club"
{{ support_email }}              # Support email address
{{ website_url }}                # Website URL
```

### Creating Custom Email Templates

**Step 1:** Create template file
```bash
# Create new template
touch club/templates/emails/custom_email.html
```

**Step 2:** Design template
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        /* Your styles */
    </style>
</head>
<body>
    <h1>Hello {{ member.firstname }}!</h1>
    <p>{{ custom_message }}</p>
</body>
</html>
```

**Step 3:** Create email function
```python
# In club/emails.py
def send_custom_email(member, custom_message):
    context = {
        'member': member,
        'custom_message': custom_message,
    }
    
    html_message = render_to_string('emails/custom_email.html', context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject='Custom Email',
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[member.email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
```

---

## Testing Emails

### Method 1: Console Backend (Current Setup)

**How to test:**

1. Start Django development server:
```bash
python manage.py runserver
```

2. Create a new member through the form

3. Check the console/terminal output:
```
Content-Type: multipart/alternative;
 boundary="===============1234567890=="
MIME-Version: 1.0
Subject: Welcome to Tennis Club, John!
From: Tennis Club <noreply@tennisclub.com>
To: john@example.com
Date: Thu, 26 Feb 2026 10:30:00 -0000

--===============1234567890==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Dear John Doe,

Welcome to Tennis Club! Your registration has been successfully completed...

--===============1234567890==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

<!DOCTYPE html>
<html>
...
</html>
```

### Method 2: File Backend (Save to Files)

**Configuration:**
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

**Result:** Emails saved as files in `sent_emails/` directory

### Method 3: Django Shell Testing

```bash
python manage.py shell
```

```python
from club.models import Names
from club.emails import send_welcome_email

# Get a member
member = Names.objects.first()

# Test email
send_welcome_email(member)

# Check console output
```

### Method 4: Unit Tests

Create `club/tests/test_emails.py`:

```python
from django.test import TestCase
from django.core import mail
from club.models import Names
from club.emails import send_welcome_email

class EmailTests(TestCase):
    def setUp(self):
        self.member = Names.objects.create(
            firstname="Test",
            lastname="User",
            email="test@example.com",
            phoneNumber="123-456-7890",
            city="Test City",
            location="Test Location"
        )
    
    def test_welcome_email_sent(self):
        """Test that welcome email is sent"""
        send_welcome_email(self.member)
        
        # Check that one email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email details
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Welcome to Tennis Club, Test!')
        self.assertEqual(email.to, ['test@example.com'])
        self.assertIn('Test User', email.body)
    
    def test_email_contains_member_info(self):
        """Test that email contains member information"""
        send_welcome_email(self.member)
        
        email = mail.outbox[0]
        self.assertIn('Test', email.body)
        self.assertIn('User', email.body)
        self.assertIn('test@example.com', email.body)
```

**Run tests:**
```bash
python manage.py test club.tests.test_emails
```

---

## Production Setup

### Step 1: Choose Email Service

**Options:**
- Gmail (free, 500 emails/day limit)
- SendGrid (free tier: 100 emails/day)
- AWS SES (pay-as-you-go, very cheap)
- Mailgun (free tier: 5,000 emails/month)
- Postmark (pay-as-you-go)

### Step 2: Get Credentials

**For Gmail:**
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate App Password:
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other"
   - Copy the 16-character password

**For SendGrid:**
1. Sign up at sendgrid.com
2. Create API key
3. Use API key as password

### Step 3: Update Settings

**Using Environment Variables (Recommended):**

```python
# settings.py
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@tennisclub.com')
```

**Set environment variables:**

Windows:
```bash
set EMAIL_HOST_USER=your-email@gmail.com
set EMAIL_HOST_PASSWORD=your-app-password
```

Linux/Mac:
```bash
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-app-password
```

### Step 4: Test Production Emails

```python
# Django shell
python manage.py shell

from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test.',
    'noreply@tennisclub.com',
    ['your-real-email@example.com'],
)
```

Check your inbox!

### Step 5: Monitor Email Delivery

**Add logging:**
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'email.log',
        },
    },
    'loggers': {
        'club.emails': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## Troubleshooting

### Problem: Emails not appearing in console

**Solution:**
1. Check `EMAIL_BACKEND` in settings.py
2. Ensure it's set to `'django.core.mail.backends.console.EmailBackend'`
3. Check terminal/console where `runserver` is running
4. Look for email output after form submission

### Problem: SMTPAuthenticationError

**Cause:** Invalid credentials or authentication failure

**Solutions:**
1. **Gmail:** Use App Password, not regular password
2. **Gmail:** Enable "Less secure app access" (not recommended)
3. Check username and password are correct
4. Verify 2FA is enabled (for Gmail)

### Problem: SMTPServerDisconnected

**Cause:** Connection to email server failed

**Solutions:**
1. Check `EMAIL_HOST` is correct
2. Verify `EMAIL_PORT` (587 for TLS, 465 for SSL)
3. Check firewall settings
4. Try different port

### Problem: Emails go to spam

**Solutions:**
1. Set up SPF records for your domain
2. Set up DKIM signing
3. Use verified sender email
4. Avoid spam trigger words
5. Include unsubscribe link
6. Use reputable email service

### Problem: Timeout errors

**Solutions:**
1. Increase `EMAIL_TIMEOUT` in settings
2. Check internet connection
3. Verify email server is accessible
4. Try different email provider

### Problem: HTML not rendering

**Cause:** Email client doesn't support HTML

**Solutions:**
1. Always include plain text version
2. Use inline CSS (not external stylesheets)
3. Test with multiple email clients
4. Use email testing services (Litmus, Email on Acid)

---

## Best Practices

### 1. Always Include Plain Text Version

```python
# Good
email = EmailMultiAlternatives(
    subject=subject,
    body=plain_message,  # Plain text version
    from_email=from_email,
    to=[recipient]
)
email.attach_alternative(html_message, "text/html")  # HTML version
```

### 2. Use Environment Variables for Credentials

```python
# Never commit credentials to version control
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

### 3. Handle Email Failures Gracefully

```python
try:
    send_welcome_email(member)
    messages.success(request, 'Email sent!')
except Exception as e:
    logger.error(f'Email failed: {e}')
    messages.warning(request, 'Email could not be sent')
    # Don't fail the entire operation
```

### 4. Log Email Activity

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f'Welcome email sent to {member.email}')
logger.error(f'Failed to send email: {str(e)}')
```

### 5. Test Emails Thoroughly

- Test in development (console backend)
- Test with real emails before production
- Test on multiple email clients
- Test spam filters
- Test unsubscribe functionality

### 6. Respect User Preferences

```python
# Add email preference field to model
class Names(models.Model):
    # ... other fields
    email_notifications = models.BooleanField(default=True)

# Check before sending
if member.email_notifications:
    send_welcome_email(member)
```

### 7. Rate Limiting

```python
# Avoid sending too many emails at once
from time import sleep

for member in members:
    send_email(member)
    sleep(0.1)  # Small delay between emails
```

### 8. Use Async for Bulk Emails

```python
# For large email campaigns
from django.core.mail import send_mass_mail

datatuple = (
    (subject1, message1, from_email, [recipient1]),
    (subject2, message2, from_email, [recipient2]),
)
send_mass_mail(datatuple)
```

---

## Summary

✅ Email system configured for development and production
✅ Welcome emails sent automatically on registration
✅ Update and deletion notifications implemented
✅ Professional HTML email templates
✅ Comprehensive error handling and logging
✅ Easy to test and deploy
✅ Scalable for future features

The email feature is now fully integrated into your Tennis Club application!
