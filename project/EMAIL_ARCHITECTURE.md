# Email System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tennis Club Email System                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   User Form  │ ───> │  Django View │ ───> │   Database   │
│  (Browser)   │      │  (views.py)  │      │  (SQLite)    │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             ├─> Save Member
                             │
                             ├─> Call send_welcome_email()
                             │
                             v
                      ┌──────────────┐
                      │ Email Module │
                      │ (emails.py)  │
                      └──────────────┘
                             │
                             ├─> Render Template
                             │
                             v
                      ┌──────────────┐
                      │   Template   │
                      │ welcome.html │
                      └──────────────┘
                             │
                             ├─> Generate HTML
                             │
                             v
                      ┌──────────────┐
                      │Email Backend │
                      │  (Console/   │
                      │    SMTP)     │
                      └──────────────┘
                             │
                             v
                      ┌──────────────┐
                      │   Recipient  │
                      │  (Console/   │
                      │   Inbox)     │
                      └──────────────┘
```

---

## Component Breakdown

### 1. User Interface Layer

```
┌─────────────────────────────────────┐
│     Create Member Form              │
│  ┌───────────────────────────────┐  │
│  │ First Name: [John          ]  │  │
│  │ Last Name:  [Doe           ]  │  │
│  │ Email:      [john@email.com]  │  │
│  │ Phone:      [123-456-7890  ]  │  │
│  │ City:       [Seattle       ]  │  │
│  │ Location:   [Downtown      ]  │  │
│  │                               │  │
│  │      [Create Member]          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 2. View Processing Layer

```python
# club/views.py

def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        
        if form.is_valid():
            # Step 1: Save to database
            member = form.save()
            
            # Step 2: Send welcome email
            email_sent = send_welcome_email(member)
            
            # Step 3: Show success message
            if email_sent:
                messages.success(request, 'Member created! Email sent.')
            
            # Step 4: Redirect
            return redirect('club:member-detail', slug=member.slug)
```

### 3. Email Module Layer

```python
# club/emails.py

def send_welcome_email(member):
    """
    ┌─────────────────────────────────┐
    │  Email Generation Process       │
    ├─────────────────────────────────┤
    │ 1. Prepare context data         │
    │ 2. Render HTML template         │
    │ 3. Create plain text version    │
    │ 4. Build email message          │
    │ 5. Send via backend             │
    │ 6. Log result                   │
    │ 7. Return success/failure       │
    └─────────────────────────────────┘
    """
    try:
        # Context data
        context = {
            'member': member,
            'club_name': 'Tennis Club',
        }
        
        # Render template
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Create email
        email = EmailMultiAlternatives(...)
        email.attach_alternative(html_message, "text/html")
        
        # Send
        email.send()
        
        return True
    except Exception as e:
        logger.error(f'Email failed: {e}')
        return False
```

### 4. Template Layer

```
┌─────────────────────────────────────────────────────────┐
│  welcome_email.html                                     │
├─────────────────────────────────────────────────────────┤
│  <!DOCTYPE html>                                        │
│  <html>                                                 │
│    <head>                                               │
│      <style>                                            │
│        /* Email-safe CSS */                            │
│      </style>                                           │
│    </head>                                              │
│    <body>                                               │
│      <div class="email-container">                     │
│        <h1>Welcome {{ member.firstname }}!</h1>        │
│        <p>Your details:</p>                            │
│        <ul>                                             │
│          <li>Email: {{ member.email }}</li>            │
│          <li>City: {{ member.city }}</li>              │
│        </ul>                                            │
│      </div>                                             │
│    </body>                                              │
│  </html>                                                │
└─────────────────────────────────────────────────────────┘
```

### 5. Email Backend Layer

```
Development Mode (Console Backend)
┌─────────────────────────────────────┐
│  EMAIL_BACKEND =                    │
│  'console.EmailBackend'             │
├─────────────────────────────────────┤
│  Output: Terminal/Console           │
│  ┌───────────────────────────────┐  │
│  │ Subject: Welcome to Club      │  │
│  │ From: noreply@club.com        │  │
│  │ To: john@example.com          │  │
│  │                               │  │
│  │ Dear John Doe,                │  │
│  │ Welcome to Tennis Club...     │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘

Production Mode (SMTP Backend)
┌─────────────────────────────────────┐
│  EMAIL_BACKEND =                    │
│  'smtp.EmailBackend'                │
├─────────────────────────────────────┤
│  Connection: SMTP Server            │
│  ┌───────────────────────────────┐  │
│  │ Connect to smtp.gmail.com:587 │  │
│  │ Authenticate with credentials │  │
│  │ Send email message            │  │
│  │ Close connection              │  │
│  └───────────────────────────────┘  │
│  Output: Recipient's Inbox          │
└─────────────────────────────────────┘
```

---

## Data Flow Diagram

### Member Registration Flow

```
User Action          System Process           Email Process
─────────────────────────────────────────────────────────────

[Fill Form]
    │
    ├─> Submit Form
    │       │
    │       ├─> Validate Data
    │       │       │
    │       │       ├─> Valid? ──> [Save to DB]
    │       │       │                   │
    │       │       │                   ├─> member.save()
    │       │       │                   │
    │       │       │                   ├─> [Trigger Email]
    │       │       │                   │       │
    │       │       │                   │       ├─> send_welcome_email(member)
    │       │       │                   │       │       │
    │       │       │                   │       │       ├─> Load Template
    │       │       │                   │       │       │
    │       │       │                   │       │       ├─> Render HTML
    │       │       │                   │       │       │
    │       │       │                   │       │       ├─> Create Email
    │       │       │                   │       │       │
    │       │       │                   │       │       ├─> Send Email
    │       │       │                   │       │       │
    │       │       │                   │       │       └─> Log Result
    │       │       │                   │       │
    │       │       │                   │       └─> Return Success
    │       │       │                   │
    │       │       │                   └─> [Show Message]
    │       │       │                           │
    │       │       │                           └─> "Member created! Email sent."
    │       │       │
    │       │       └─> Invalid? ──> [Show Errors]
    │       │
    │       └─> [Redirect to Detail Page]
    │
    └─> [View Member Profile]
```

---

## Email Types and Triggers

```
┌──────────────────────────────────────────────────────────────┐
│                    Email Event Matrix                         │
├──────────────┬─────────────────┬──────────────────────────────┤
│   Action     │   Trigger       │   Email Function             │
├──────────────┼─────────────────┼──────────────────────────────┤
│ Create       │ Form Submit     │ send_welcome_email()         │
│ Member       │ (POST)          │ → welcome_email.html         │
├──────────────┼─────────────────┼──────────────────────────────┤
│ Update       │ Edit Form       │ send_member_update_          │
│ Member       │ Submit (POST)   │ notification()               │
├──────────────┼─────────────────┼──────────────────────────────┤
│ Delete       │ Confirm Delete  │ send_deletion_               │
│ Member       │ (POST)          │ confirmation()               │
├──────────────┼─────────────────┼──────────────────────────────┤
│ Bulk         │ Admin Action    │ send_bulk_email()            │
│ Announce     │ (Manual)        │                              │
└──────────────┴─────────────────┴──────────────────────────────┘
```

---

## Configuration Layers

```
┌─────────────────────────────────────────────────────────────┐
│                  Configuration Stack                         │
└─────────────────────────────────────────────────────────────┘

Layer 1: Django Settings (project/settings.py)
┌─────────────────────────────────────────────────────────────┐
│ EMAIL_BACKEND = 'django.core.mail.backends.console...'     │
│ EMAIL_HOST = 'smtp.gmail.com'                              │
│ EMAIL_PORT = 587                                            │
│ EMAIL_USE_TLS = True                                        │
│ EMAIL_HOST_USER = 'your-email@gmail.com'                   │
│ EMAIL_HOST_PASSWORD = 'your-app-password'                  │
│ DEFAULT_FROM_EMAIL = 'Tennis Club <noreply@club.com>'      │
└─────────────────────────────────────────────────────────────┘
                            │
                            v
Layer 2: Email Module (club/emails.py)
┌─────────────────────────────────────────────────────────────┐
│ def send_welcome_email(member):                             │
│     subject = f'Welcome to Tennis Club, {member.firstname}!'│
│     context = {'member': member, ...}                       │
│     html_message = render_to_string('emails/welcome...')   │
│     email = EmailMultiAlternatives(...)                     │
│     email.send()                                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            v
Layer 3: Email Template (club/templates/emails/welcome_email.html)
┌─────────────────────────────────────────────────────────────┐
│ <html>                                                      │
│   <body>                                                    │
│     <h1>Welcome {{ member.firstname }}!</h1>               │
│     <p>Your email: {{ member.email }}</p>                  │
│   </body>                                                   │
│ </html>                                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            v
Layer 4: Email Backend (Django Core)
┌─────────────────────────────────────────────────────────────┐
│ Console Backend: Print to terminal                         │
│ SMTP Backend: Send via email server                        │
│ File Backend: Save to file                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
send_welcome_email(member)
    │
    ├─> try:
    │       │
    │       ├─> Prepare context
    │       │       │
    │       │       └─> Success ──> Continue
    │       │
    │       ├─> Render template
    │       │       │
    │       │       ├─> Success ──> Continue
    │       │       │
    │       │       └─> Error ──> TemplateDoesNotExist
    │       │                         │
    │       │                         └─> Catch in except block
    │       │
    │       ├─> Create email
    │       │       │
    │       │       └─> Success ──> Continue
    │       │
    │       ├─> Send email
    │       │       │
    │       │       ├─> Success ──> Log success
    │       │       │                   │
    │       │       │                   └─> Return True
    │       │       │
    │       │       └─> Error ──> SMTPException
    │       │                         │
    │       │                         └─> Catch in except block
    │       │
    │       └─> Return True
    │
    └─> except Exception as e:
            │
            ├─> Log error
            │       │
            │       └─> logger.error(f'Failed: {e}')
            │
            └─> Return False
```

---

## Deployment Environments

```
┌─────────────────────────────────────────────────────────────┐
│                    Environment Matrix                        │
├─────────────────┬───────────────────┬───────────────────────┤
│  Environment    │  Email Backend    │  Purpose              │
├─────────────────┼───────────────────┼───────────────────────┤
│  Development    │  Console          │  Testing, debugging   │
│  (Local)        │  Backend          │  No real emails sent  │
├─────────────────┼───────────────────┼───────────────────────┤
│  Testing        │  File Backend     │  Automated tests      │
│  (CI/CD)        │  or Locmem        │  Email verification   │
├─────────────────┼───────────────────┼───────────────────────┤
│  Staging        │  SMTP Backend     │  Pre-production test  │
│  (Test Server)  │  (Test account)   │  Real email testing   │
├─────────────────┼───────────────────┼───────────────────────┤
│  Production     │  SMTP Backend     │  Live emails to users │
│  (Live Server)  │  (Production)     │  Real email service   │
└─────────────────┴───────────────────┴───────────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
└─────────────────────────────────────────────────────────────┘

Layer 1: Credential Protection
┌─────────────────────────────────────────────────────────────┐
│ ✓ Environment variables for passwords                       │
│ ✓ Never commit credentials to Git                          │
│ ✓ Use .env files (not in version control)                  │
│ ✓ App passwords instead of account passwords               │
└─────────────────────────────────────────────────────────────┘

Layer 2: Connection Security
┌─────────────────────────────────────────────────────────────┐
│ ✓ TLS encryption (EMAIL_USE_TLS = True)                    │
│ ✓ Secure ports (587 for TLS, 465 for SSL)                  │
│ ✓ Timeout settings (EMAIL_TIMEOUT = 10)                    │
└─────────────────────────────────────────────────────────────┘

Layer 3: Content Security
┌─────────────────────────────────────────────────────────────┐
│ ✓ HTML escaping in templates                               │
│ ✓ No user input in email headers                           │
│ ✓ Validate email addresses                                 │
│ ✓ Rate limiting for bulk emails                            │
└─────────────────────────────────────────────────────────────┘

Layer 4: Error Handling
┌─────────────────────────────────────────────────────────────┐
│ ✓ Try-except blocks                                         │
│ ✓ Logging (not exposing to users)                          │
│ ✓ Graceful degradation                                      │
│ ✓ User-friendly error messages                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Performance Considerations

```
┌─────────────────────────────────────────────────────────────┐
│              Email Performance Optimization                  │
└─────────────────────────────────────────────────────────────┘

Single Email (Current Implementation)
┌─────────────────────────────────────────────────────────────┐
│ User Action → Save Member → Send Email → Response          │
│ Time: ~1-2 seconds                                          │
│ Blocking: Yes (user waits)                                  │
│ Suitable for: Individual registrations                      │
└─────────────────────────────────────────────────────────────┘

Async Email (Future Enhancement)
┌─────────────────────────────────────────────────────────────┐
│ User Action → Save Member → Queue Email → Response         │
│                                    ↓                        │
│                            Background Worker                │
│                                    ↓                        │
│                              Send Email                     │
│ Time: ~0.5 seconds (user response)                          │
│ Blocking: No (immediate response)                           │
│ Suitable for: High-volume operations                        │
└─────────────────────────────────────────────────────────────┘

Bulk Email (send_bulk_email function)
┌─────────────────────────────────────────────────────────────┐
│ Admin Action → Prepare List → Send Batch → Response        │
│ Time: Varies by count                                       │
│ Optimization: send_mass_mail() for efficiency              │
│ Suitable for: Announcements, newsletters                    │
└─────────────────────────────────────────────────────────────┘
```

This architecture provides a solid foundation for email functionality that can scale from development to production!
