# Authentication System Guide

## Overview

Your Tennis Club application now has a complete authentication system that works alongside the existing form-based member creation. Users can register accounts, login, and access protected features.

## Two Ways to Interact with the App

### 1. Form-Based Member Creation (Existing)
- **Purpose**: Admin/staff creates member profiles
- **URL**: `/member/create/`
- **Features**: Creates member records in the `Names` model
- **No authentication required**: Anyone can access (you may want to protect this later)

### 2. User Authentication System (New)
- **Purpose**: Users create their own accounts and login
- **Features**: 
  - User registration with email verification
  - Secure password hashing
  - Login/logout functionality
  - User profiles
  - Welcome emails sent on registration

## Key Differences

| Feature | Member Creation (Form) | User Registration (Auth) |
|---------|----------------------|-------------------------|
| Model | `Names` (club members) | `User` (Django built-in) |
| Password | No password | Hashed password |
| Purpose | Member directory | Account access |
| Email Use | Contact info | Login + notifications |
| Created By | Admin/Staff | Self-registration |

## Authentication URLs

```
/register/          - Create new user account
/login/             - Login to existing account
/logout/            - Logout from account
/profile/           - View user profile (requires login)
```

## How It Works

### User Registration Flow

1. User visits `/register/`
2. Fills out registration form:
   - Username (required)
   - Email (required, must be unique)
   - First name (optional)
   - Last name (optional)
   - Password (required, validated)
   - Password confirmation (required)
3. Form validates:
   - Email uniqueness
   - Password strength (min 8 chars, not all numeric)
   - Password match
4. User account created with hashed password
5. Welcome email sent to user's email
6. User automatically logged in
7. Redirected to homepage

### Login Flow

1. User visits `/login/`
2. Enters username and password
3. Credentials validated
4. If valid: logged in and redirected to homepage
5. If invalid: error message shown

### Logout Flow

1. User clicks logout link
2. Confirmation page shown
3. User confirms logout
4. Session cleared
5. Redirected to homepage

## Files Created

### Forms
- `club/auth_forms.py` - Registration and login forms

### Views
- `club/auth_views.py` - Authentication view functions
  - `register_view()` - Handle registration
  - `login_view()` - Handle login
  - `logout_view()` - Handle logout
  - `profile_view()` - Display user profile

### Templates
- `club/templates/auth/register.html` - Registration page
- `club/templates/auth/login.html` - Login page
- `club/templates/auth/logout_confirm.html` - Logout confirmation
- `club/templates/auth/profile.html` - User profile page

### Email Functions
- `club/emails.py` - Added `send_welcome_email_to_user()`

### URL Configuration
- `club/urls.py` - Added authentication routes

## Security Features

### Password Security
- Passwords are hashed using Django's PBKDF2 algorithm
- Never stored in plain text
- Validated for strength:
  - Minimum 8 characters
  - Can't be entirely numeric
  - Can't be too similar to username
  - Can't be a common password

### Session Security
- Sessions managed by Django
- CSRF protection on all forms
- Secure cookies (when HTTPS enabled)

### Email Validation
- Email must be unique
- Valid email format required
- Used for account recovery (future feature)

## Using Authentication in Views

### Protect Views (Require Login)

```python
from django.contrib.auth.decorators import login_required

@login_required
def protected_view(request):
    # Only logged-in users can access this
    return render(request, 'template.html')
```

### Check if User is Logged In (Template)

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    <a href="{% url 'club:logout' %}">Logout</a>
{% else %}
    <a href="{% url 'club:login' %}">Login</a>
    <a href="{% url 'club:register' %}">Register</a>
{% endif %}
```

### Check if User is Logged In (View)

```python
def my_view(request):
    if request.user.is_authenticated:
        # User is logged in
        username = request.user.username
        email = request.user.email
    else:
        # User is not logged in
        pass
```

## Testing the Authentication System

### 1. Create a Test User

```bash
# Option 1: Through the web interface
# Visit: http://localhost:8000/register/

# Option 2: Through Django shell
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User'
)
```

### 2. Test Login

1. Visit `http://localhost:8000/login/`
2. Enter credentials
3. Should redirect to homepage with welcome message

### 3. Test Profile

1. While logged in, visit `http://localhost:8000/profile/`
2. Should see user information

### 4. Test Logout

1. Click logout link
2. Confirm logout
3. Should redirect to homepage

## Email Configuration

Currently using console backend (emails print to terminal):

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### To Enable Real Emails (Gmail Example)

Update `project/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Not your regular password!
DEFAULT_FROM_EMAIL = 'Tennis Club <your-email@gmail.com>'
```

**Important**: Use an App Password, not your regular Gmail password!
1. Enable 2-factor authentication on Gmail
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use that password in settings

## Protecting Member Creation

Currently, anyone can create members via the form. To restrict this to logged-in users:

```python
# In club/views.py
from django.contrib.auth.decorators import login_required

@login_required
def create_member(request):
    # ... existing code ...
```

To restrict to admin users only:

```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def create_member(request):
    # ... existing code ...
```

## Future Enhancements

### Password Reset
Add password reset functionality:
- Forgot password link
- Email with reset token
- Reset password form

### Email Verification
Require email verification before login:
- Send verification email on registration
- User clicks link to verify
- Account activated

### User Permissions
Add role-based access:
- Regular members
- Staff members
- Administrators

### Social Authentication
Allow login with:
- Google
- Facebook
- GitHub

### Two-Factor Authentication
Add extra security layer:
- SMS verification
- Authenticator app
- Email codes

## Common Issues

### "User already exists" Error
- Email or username already registered
- Try different username/email
- Or login with existing account

### Email Not Sending
- Check EMAIL_BACKEND setting
- Verify SMTP credentials
- Check spam folder
- Look at console output (console backend)

### "CSRF verification failed"
- Ensure `{% csrf_token %}` in all forms
- Check CSRF middleware is enabled
- Clear browser cookies

### Can't Access Protected Pages
- Ensure you're logged in
- Check LOGIN_URL setting
- Verify @login_required decorator

## Database Tables

### User Table (Django Built-in)
Stores authentication data:
- username
- email
- password (hashed)
- first_name
- last_name
- date_joined
- last_login
- is_active
- is_staff
- is_superuser

### Names Table (Your Custom Model)
Stores member data:
- firstname
- lastname
- email
- phoneNumber
- city
- location
- slug
- status
- profile_picture
- date_joined
- date_updated
- date_started

## Linking Users and Members (Future)

You may want to link User accounts to Member profiles:

```python
# In club/models.py
from django.contrib.auth.models import User

class Names(models.Model):
    # ... existing fields ...
    
    # Add this field to link to User
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='member_profile'
    )
```

Then run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Admin Interface

Create a superuser to access Django admin:

```bash
python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin/` to:
- View all users
- Edit user permissions
- Manage user accounts
- View member records

## Summary

You now have two parallel systems:

1. **Member Management** (existing)
   - Form-based member creation
   - Member directory
   - Member profiles with photos
   - Email notifications

2. **User Authentication** (new)
   - User registration
   - Login/logout
   - User profiles
   - Secure password handling
   - Welcome emails

Both systems work independently but can be integrated in the future by linking User accounts to Member profiles.

## Next Steps

1. Test the registration flow
2. Test login/logout
3. Configure real email sending (optional)
4. Protect member creation with @login_required
5. Consider linking Users to Members
6. Add password reset functionality
7. Customize email templates
8. Add user profile editing

---

**Need Help?**
- Check Django authentication docs: https://docs.djangoproject.com/en/stable/topics/auth/
- Review the code in `club/auth_views.py` and `club/auth_forms.py`
- Test in Django shell: `python manage.py shell`
