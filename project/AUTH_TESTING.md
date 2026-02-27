# Authentication System Testing Guide

## Quick Test Checklist

Use this checklist to verify the authentication system works correctly.

### ✅ Pre-Test Setup

```bash
# 1. Navigate to project directory
cd project

# 2. Start development server
python manage.py runserver

# 3. Open browser to http://localhost:8000/
```

---

## Test 1: User Registration

### Steps
1. Visit `http://localhost:8000/register/`
2. Fill out the form:
   - Username: `testuser1`
   - Email: `test1@example.com`
   - First Name: `Test` (optional)
   - Last Name: `User` (optional)
   - Password: `SecurePass123`
   - Confirm Password: `SecurePass123`
3. Click "Create Account"

### Expected Results
- ✅ Redirected to homepage
- ✅ Success message: "Welcome testuser1! Your account has been created..."
- ✅ Navigation shows: "Welcome, testuser1!" with Profile and Logout links
- ✅ Console shows welcome email output

### Check Console Output
```
============================================================
SENDING USER REGISTRATION WELCOME EMAIL
============================================================
Username: testuser1
Email: test1@example.com
Subject: Welcome to Tennis Club, testuser1!
Sending email...
✅ Email sent successfully!
============================================================
```

---

## Test 2: Logout

### Steps
1. Click "Logout" link in navigation
2. Confirm logout on confirmation page
3. Click "Yes, Logout"

### Expected Results
- ✅ Redirected to homepage
- ✅ Success message: "Goodbye, testuser1! You have been logged out."
- ✅ Navigation shows: "Login" and "Register" links
- ✅ User is logged out

---

## Test 3: Login

### Steps
1. Visit `http://localhost:8000/login/`
2. Enter credentials:
   - Username: `testuser1`
   - Password: `SecurePass123`
3. Click "Login"

### Expected Results
- ✅ Redirected to homepage
- ✅ Success message: "Welcome back, testuser1!"
- ✅ Navigation shows: "Welcome, testuser1!" with Profile and Logout links
- ✅ User is logged in

---

## Test 4: View Profile

### Steps
1. While logged in, visit `http://localhost:8000/profile/`
2. Or click "Profile" link in navigation

### Expected Results
- ✅ Profile page displays
- ✅ Shows username: `testuser1`
- ✅ Shows email: `test1@example.com`
- ✅ Shows name (if provided)
- ✅ Shows date joined
- ✅ Shows last login

---

## Test 5: Protected Page Access

### Steps
1. Logout if logged in
2. Try to visit `http://localhost:8000/profile/`

### Expected Results
- ✅ Redirected to login page
- ✅ URL shows: `/login/?next=/profile/`
- ✅ After login, redirected back to profile

---

## Test 6: Form Validation

### Test 6a: Duplicate Username
1. Visit `/register/`
2. Try to register with username: `testuser1` (already exists)
3. Use different email: `test2@example.com`

**Expected**: Error message about username already exists

### Test 6b: Duplicate Email
1. Visit `/register/`
2. Use new username: `testuser2`
3. Try to use email: `test1@example.com` (already exists)

**Expected**: Error message "This email is already registered."

### Test 6c: Password Mismatch
1. Visit `/register/`
2. Password: `SecurePass123`
3. Confirm Password: `DifferentPass456`

**Expected**: Error message about passwords not matching

### Test 6d: Weak Password
1. Visit `/register/`
2. Try password: `123` (too short)

**Expected**: Error message about password length

### Test 6e: Invalid Email
1. Visit `/register/`
2. Email: `notanemail` (invalid format)

**Expected**: Error message about invalid email format

---

## Test 7: Login Validation

### Test 7a: Wrong Password
1. Visit `/login/`
2. Username: `testuser1`
3. Password: `WrongPassword`

**Expected**: Error message "Invalid username or password."

### Test 7b: Non-existent User
1. Visit `/login/`
2. Username: `nonexistent`
3. Password: `anything`

**Expected**: Error message "Invalid username or password."

---

## Test 8: Email Functionality

### Test 8a: Console Backend (Current)
1. Register a new user
2. Check terminal/console output
3. Look for email content

**Expected**: Full email HTML printed to console

### Test 8b: SMTP Backend (Optional)
1. Configure SMTP in settings.py
2. Register a new user
3. Check email inbox

**Expected**: Welcome email received in inbox

---

## Test 9: Session Persistence

### Steps
1. Login as `testuser1`
2. Navigate to different pages
3. Close browser tab
4. Reopen `http://localhost:8000/`

### Expected Results
- ✅ Still logged in (session persists)
- ✅ Navigation shows logged-in state
- ✅ Can access profile without re-login

---

## Test 10: Multiple Users

### Steps
1. Register multiple users:
   - `testuser1` / `test1@example.com`
   - `testuser2` / `test2@example.com`
   - `testuser3` / `test3@example.com`
2. Login as each user
3. View each profile

### Expected Results
- ✅ Each user has separate account
- ✅ Each user sees their own profile
- ✅ No data mixing between users

---

## Test 11: Navigation Links

### Test 11a: Not Logged In
Visit homepage and check navigation

**Expected Links**:
- Login
- Register

### Test 11b: Logged In
Login and check navigation

**Expected Links**:
- Welcome, [username]!
- Profile
- Logout

---

## Test 12: CSRF Protection

### Steps
1. Open browser developer tools
2. Go to `/register/`
3. Inspect form HTML
4. Look for hidden input with name `csrfmiddlewaretoken`

### Expected Results
- ✅ CSRF token present in form
- ✅ Token is long random string
- ✅ Form submission includes token

---

## Test 13: Password Security

### Steps
1. Register a user
2. Open Django shell:
   ```bash
   python manage.py shell
   ```
3. Check password storage:
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(username='testuser1')
   print(user.password)
   ```

### Expected Results
- ✅ Password is hashed (not plain text)
- ✅ Format: `pbkdf2_sha256$260000$salt$hash`
- ✅ Cannot reverse hash to get original password

---

## Test 14: Admin Interface

### Steps
1. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
2. Visit `http://localhost:8000/admin/`
3. Login with superuser credentials
4. Navigate to Users section

### Expected Results
- ✅ Can see all registered users
- ✅ Can edit user details
- ✅ Can see password hashes (not plain text)
- ✅ Can manage user permissions

---

## Test 15: Integration with Members

### Current Behavior
1. Visit `/member/create/`
2. Create a member (no login required)

**Expected**: Works without authentication

### Future Behavior (After Protection)
Add `@login_required` to `create_member` view:
1. Logout
2. Try to visit `/member/create/`

**Expected**: Redirected to login page

---

## Automated Testing (Optional)

Create test file `club/test_auth.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_registration(self):
        response = self.client.post(reverse('club:register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login(self):
        response = self.client.post(reverse('club:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_profile_requires_login(self):
        response = self.client.get(reverse('club:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('club:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect
```

Run tests:
```bash
python manage.py test club.test_auth
```

---

## Performance Testing

### Test Load Time
1. Open browser developer tools
2. Go to Network tab
3. Visit authentication pages
4. Check load times

**Expected**: All pages load in < 1 second

### Test Database Queries
1. Install Django Debug Toolbar (optional)
2. Check number of queries per page

**Expected**: Minimal queries (1-3 per page)

---

## Security Testing

### Test 1: SQL Injection
Try entering SQL in username field:
```
' OR '1'='1
```

**Expected**: Treated as literal string, not executed

### Test 2: XSS Attack
Try entering script in username:
```
<script>alert('XSS')</script>
```

**Expected**: Escaped and displayed as text

### Test 3: CSRF Attack
Try submitting form without CSRF token

**Expected**: 403 Forbidden error

---

## Browser Compatibility

Test in multiple browsers:
- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge

**Expected**: Works consistently across all browsers

---

## Mobile Responsiveness

Test on mobile devices or use browser dev tools:
1. Toggle device toolbar
2. Test on various screen sizes
3. Check form usability

**Expected**: Forms are usable on mobile devices

---

## Common Issues & Solutions

### Issue: "CSRF verification failed"
**Solution**: 
- Clear browser cookies
- Ensure `{% csrf_token %}` in forms
- Check CSRF middleware enabled

### Issue: "User already exists"
**Solution**: 
- Use different username/email
- Or delete existing user in admin

### Issue: Email not sending
**Solution**: 
- Check console output (console backend)
- Verify SMTP settings (SMTP backend)
- Check EMAIL_BACKEND setting

### Issue: Can't access profile
**Solution**: 
- Ensure you're logged in
- Check LOGIN_URL setting
- Verify @login_required decorator

---

## Test Results Template

Use this template to track your testing:

```
Date: _______________
Tester: _______________

[ ] Test 1: User Registration
[ ] Test 2: Logout
[ ] Test 3: Login
[ ] Test 4: View Profile
[ ] Test 5: Protected Page Access
[ ] Test 6: Form Validation
[ ] Test 7: Login Validation
[ ] Test 8: Email Functionality
[ ] Test 9: Session Persistence
[ ] Test 10: Multiple Users
[ ] Test 11: Navigation Links
[ ] Test 12: CSRF Protection
[ ] Test 13: Password Security
[ ] Test 14: Admin Interface
[ ] Test 15: Integration with Members

Issues Found:
_________________________________
_________________________________
_________________________________

Notes:
_________________________________
_________________________________
_________________________________
```

---

## Next Steps After Testing

Once all tests pass:
1. ✅ Configure production email (SMTP)
2. ✅ Add @login_required to protected views
3. ✅ Customize email templates
4. ✅ Add password reset functionality
5. ✅ Deploy to production
6. ✅ Monitor for issues

---

**Testing Complete?** 
Read `AUTHENTICATION_GUIDE.md` for customization options and advanced features!
