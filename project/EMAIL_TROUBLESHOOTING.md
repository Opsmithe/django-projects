# Email Troubleshooting Guide

## Issue: Email Not Printing to Terminal

### Quick Diagnostic Steps

#### Step 1: Run the Test Script

```bash
cd project
python test_email.py
```

This will:
- Check your email configuration
- Test sending an email to the most recent member
- Show detailed output of what's happening

#### Step 2: Check Terminal Output

When you create a member, you should see:

```
============================================================
SENDING WELCOME EMAIL
============================================================
Recipient: John Doe
Email: john@example.com
Subject: Welcome to Tennis Club, John!
Rendering email template...
Creating email message...
Sending email...
✅ Email sent successfully!
============================================================

[Then the actual email content will be printed below]
```

### Common Issues and Solutions

#### Issue 1: No Output at All

**Symptom:** Nothing prints when creating a member

**Possible Causes:**
1. Email function not being called
2. Silent exception being caught
3. Wrong terminal window

**Solutions:**

**A. Check you're looking at the right terminal**
- Make sure you're looking at the terminal where `python manage.py runserver` is running
- NOT the terminal where you opened the browser

**B. Verify the function is being called**
```bash
# Add this to views.py temporarily
def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            print("DEBUG: About to send email...")  # ADD THIS
            email_sent = send_welcome_email(member)
            print(f"DEBUG: Email sent result: {email_sent}")  # ADD THIS
```

**C. Check for import errors**
```bash
python manage.py shell
```
```python
from club.emails import send_welcome_email
# If this fails, there's an import error
```

#### Issue 2: Error Messages Appear

**Symptom:** You see error messages in terminal

**Common Errors:**

**A. TemplateDoesNotExist: emails/welcome_email.html**

**Solution:**
```bash
# Check if template exists
ls club/templates/emails/welcome_email.html

# If not found, create the directory
mkdir -p club/templates/emails

# Then create the template (see EMAIL_GUIDE.md)
```

**B. AttributeError: 'Names' object has no attribute 'email'**

**Solution:**
```bash
# Check if email field exists in model
python manage.py shell
```
```python
from club.models import Names
member = Names.objects.first()
print(member.email)  # Should print email
```

If error occurs, run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

**C. ImportError: cannot import name 'send_welcome_email'**

**Solution:**
Check that `club/emails.py` exists and has the function defined.

#### Issue 3: Email Sent But Not Visible

**Symptom:** Success message shows but no email in terminal

**Possible Causes:**
1. Wrong email backend
2. Output being redirected
3. Terminal buffer issue

**Solutions:**

**A. Verify email backend**
```bash
python manage.py shell
```
```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
# Should print: django.core.mail.backends.console.EmailBackend
```

**B. Try file backend instead**
```python
# In settings.py, temporarily change to:
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

Then check the `sent_emails/` directory for email files.

**C. Check terminal buffer**
- Scroll up in terminal
- Email might be printed above
- Try clearing terminal and testing again

#### Issue 4: Member Created But No Email Function Called

**Symptom:** Member appears in database but no email activity

**Possible Causes:**
1. Form validation failing silently
2. Redirect happening before email
3. Exception being caught

**Solutions:**

**A. Add debug prints**
```python
# In views.py create_member function
if form.is_valid():
    print("DEBUG: Form is valid")
    member = form.save()
    print(f"DEBUG: Member saved: {member}")
    print(f"DEBUG: Member email: {member.email}")
    email_sent = send_welcome_email(member)
    print(f"DEBUG: Email result: {email_sent}")
```

**B. Check form validation**
```python
if request.method == 'POST':
    form = MemberForm(request.POST)
    print(f"DEBUG: Form data: {request.POST}")
    print(f"DEBUG: Form is valid: {form.is_valid()}")
    if not form.is_valid():
        print(f"DEBUG: Form errors: {form.errors}")
```

### Manual Testing

#### Test 1: Direct Email Function Call

```bash
python manage.py shell
```

```python
from club.models import Names
from club.emails import send_welcome_email

# Get any member
member = Names.objects.first()

# Try sending email
result = send_welcome_email(member)

# Check result
print(f"Result: {result}")
```

You should see the email printed immediately.

#### Test 2: Test Django Email System

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body',
    'from@example.com',
    ['to@example.com'],
)
```

You should see:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Test Subject
From: from@example.com
To: to@example.com
Date: ...

Test message body
```

#### Test 3: Check Email Configuration

```bash
python manage.py shell
```

```python
from django.conf import settings

print("Email Backend:", settings.EMAIL_BACKEND)
print("Default From:", settings.DEFAULT_FROM_EMAIL)
print("Email Timeout:", settings.EMAIL_TIMEOUT)
```

Expected output:
```
Email Backend: django.core.mail.backends.console.EmailBackend
Default From: Tennis Club <noreply@tennisclub.com>
Email Timeout: 10
```

### Verification Checklist

Run through this checklist:

- [ ] `EMAIL_BACKEND` is set to `'django.core.mail.backends.console.EmailBackend'`
- [ ] `club/emails.py` file exists
- [ ] `club/templates/emails/welcome_email.html` exists
- [ ] `send_welcome_email` is imported in `views.py`
- [ ] `send_welcome_email(member)` is called in `create_member` view
- [ ] Looking at correct terminal (where runserver is running)
- [ ] No import errors when importing email functions
- [ ] Member has valid email address
- [ ] Form validation is passing

### Still Not Working?

#### Enable Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

```python
# In settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = ['127.0.0.1']
```

```python
# In urls.py
from django.urls import include

urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
```

This will show you detailed information about what's happening.

#### Check Django Logs

```python
# In settings.py, add:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'club.emails': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Get Help

If none of these solutions work:

1. Run the test script: `python test_email.py`
2. Copy the full output
3. Check for any error messages
4. Look for the debug print statements
5. Share the output for further diagnosis

### Quick Fix: Alternative Email Backend

If console backend isn't working, try file backend:

```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

Create a member, then check:
```bash
ls sent_emails/
cat sent_emails/*
```

You should see email files there.
