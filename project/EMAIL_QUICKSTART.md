# Email Feature - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### What You Get

When a new member registers, they automatically receive a professional welcome email with:
- Personalized greeting
- Registration details
- Getting started guide
- Contact information

---

## ✅ Current Setup (Development)

Your email system is **already configured** for development!

**Configuration:** Emails print to console (no setup needed)

**Location:** `project/settings.py`
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 🧪 Testing the Email Feature

### Step 1: Start the Server

```bash
cd project
python manage.py runserver
```

### Step 2: Create a New Member

1. Visit: `http://localhost:8000/create/`
2. Fill out the form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Phone: 123-456-7890
   - City: Seattle
   - Location: Downtown
3. Click "Create Member"

### Step 3: Check the Console

Look at your terminal where `runserver` is running. You'll see:

```
Content-Type: multipart/alternative;
Subject: Welcome to Tennis Club, John!
From: Tennis Club <noreply@tennisclub.com>
To: john@example.com

Dear John Doe,

Welcome to Tennis Club! Your registration has been successfully completed...
```

**That's it!** The email was "sent" (printed to console).

---

## 📧 Email Functions Available

### 1. Welcome Email (Automatic)
Sent when creating a new member via the form.

### 2. Update Notification (Automatic)
Sent when editing member information.

### 3. Deletion Confirmation (Automatic)
Sent when deleting a member account.

### 4. Manual Email (Code)
```python
from club.emails import send_welcome_email
from club.models import Names

member = Names.objects.get(id=1)
send_welcome_email(member)
```

---

## 🌐 Production Setup (When Ready)

### For Gmail (Free)

**Step 1:** Get App Password
1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate App Password (select "Mail" and "Other")
4. Copy the 16-character password

**Step 2:** Update Settings
Edit `project/settings.py`:

```python
# Comment out console backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Uncomment and configure SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
DEFAULT_FROM_EMAIL = 'Tennis Club <your-email@gmail.com>'
```

**Step 3:** Test
Create a new member and check your real email inbox!

---

## 📁 File Structure

```
project/
├── club/
│   ├── emails.py                          # Email functions
│   └── templates/
│       └── emails/
│           └── welcome_email.html         # Email template
├── project/
│   └── settings.py                        # Email configuration
├── EMAIL_GUIDE.md                         # Full documentation
└── EMAIL_QUICKSTART.md                    # This file
```

---

## 🔧 Common Tasks

### View Email in Browser

1. Copy HTML from console output
2. Save as `test_email.html`
3. Open in browser

### Send Test Email

```bash
python manage.py shell
```

```python
from club.models import Names
from club.emails import send_welcome_email

member = Names.objects.first()
send_welcome_email(member)
```

### Check Email Logs

```python
import logging
logger = logging.getLogger('club.emails')
# Logs are in club/emails.py
```

---

## ❓ Troubleshooting

### Emails not showing in console?
- Check terminal where `runserver` is running
- Verify `EMAIL_BACKEND` in settings.py
- Look for success message after creating member

### Want to see HTML version?
- Copy HTML from console
- Save to file and open in browser
- Or switch to file backend (see EMAIL_GUIDE.md)

### Ready for production?
- See "Production Setup" section above
- Or read full EMAIL_GUIDE.md

---

## 📚 Learn More

- **Full Documentation:** `EMAIL_GUIDE.md`
- **Email Functions:** `club/emails.py`
- **Email Template:** `club/templates/emails/welcome_email.html`
- **Settings:** `project/settings.py`

---

## ✨ Features

✅ Automatic welcome emails
✅ Update notifications
✅ Deletion confirmations
✅ Professional HTML templates
✅ Plain text fallback
✅ Error handling
✅ Logging
✅ Easy to customize

**You're all set!** The email feature is ready to use.
