# Authentication Quick Start

## What Was Added

Your app now has user authentication! Users can register accounts, login, and logout.

## Try It Now

### 1. Start the Server

```bash
cd project
python manage.py runserver
```

### 2. Register a New Account

1. Visit: `http://localhost:8000/register/`
2. Fill out the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - Confirm password: `testpass123`
3. Click "Create Account"
4. You'll be automatically logged in!

### 3. Check the Welcome Email

Look at your terminal/console - you'll see the welcome email that was "sent" (currently emails just print to console).

### 4. View Your Profile

1. Visit: `http://localhost:8000/profile/`
2. See your account information

### 5. Logout

1. Click the "Logout" link in the navigation
2. Confirm logout

### 6. Login Again

1. Visit: `http://localhost:8000/login/`
2. Enter your username and password
3. Click "Login"

## Key URLs

```
/register/  - Create new account
/login/     - Login
/logout/    - Logout
/profile/   - View profile (must be logged in)
```

## Navigation

The homepage now shows:
- **Not logged in**: "Login" and "Register" links
- **Logged in**: "Welcome, [username]!", "Profile", and "Logout" links

## Two Systems Working Together

### Member Creation (Existing)
- URL: `/member/create/`
- Creates member profiles (Names model)
- No password required
- For admin/staff use

### User Registration (New)
- URL: `/register/`
- Creates user accounts (User model)
- Password required (hashed)
- For self-registration

Both systems work independently!

## What's Protected

Currently, nothing requires login. To protect a page:

```python
# In views.py
from django.contrib.auth.decorators import login_required

@login_required
def my_protected_view(request):
    # Only logged-in users can access
    return render(request, 'template.html')
```

## Enable Real Emails

Currently emails print to console. To send real emails, update `project/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Files Added

- `club/auth_forms.py` - Registration/login forms
- `club/auth_views.py` - Authentication views
- `club/templates/auth/` - Authentication templates
- `club/emails.py` - Updated with user welcome email
- `AUTHENTICATION_GUIDE.md` - Full documentation

## Next Steps

1. Test registration and login
2. Protect member creation with `@login_required`
3. Configure real email sending
4. Customize the templates
5. Add password reset functionality

## Need More Info?

Read `AUTHENTICATION_GUIDE.md` for complete documentation!
