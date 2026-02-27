# Authentication System Flow Diagrams

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Tennis Club Application                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │  Member Management   │      │  User Authentication │    │
│  │     (Existing)       │      │       (New)          │    │
│  ├──────────────────────┤      ├──────────────────────┤    │
│  │ Model: Names         │      │ Model: User          │    │
│  │ No password          │      │ Hashed password      │    │
│  │ Form-based creation  │      │ Self-registration    │    │
│  │ Member directory     │      │ Account access       │    │
│  └──────────────────────┘      └──────────────────────┘    │
│                                                               │
│  Both systems work independently but can be linked later     │
└─────────────────────────────────────────────────────────────┘
```

## Registration Flow

```
User Action                 System Process                  Result
───────────                ────────────────               ────────

Visit /register/
      │
      ├──────────────────> Display registration form
      │
Fill out form:
- Username
- Email
- Password
- Confirm password
      │
      ├──────────────────> Validate form data
      │                    ├─ Check username unique
      │                    ├─ Check email unique
      │                    ├─ Validate password strength
      │                    └─ Check passwords match
      │
Submit form                         │
      │                             │
      ├─────────────────────────────┤
      │                             │
      │                    Create User object
      │                    ├─ Hash password (PBKDF2)
      │                    ├─ Save to database
      │                    └─ Generate session
      │                             │
      │                    Send welcome email
      │                    ├─ Render email template
      │                    ├─ Send via EMAIL_BACKEND
      │                    └─ Log result
      │                             │
      │                    Auto-login user
      │                    └─ Create session cookie
      │                             │
      │<─────────────────────────────┤
      │
Redirected to homepage
with success message
      │
      ▼
✓ Account created
✓ Logged in
✓ Welcome email sent
```

## Login Flow

```
User Action                 System Process                  Result
───────────                ────────────────               ────────

Visit /login/
      │
      ├──────────────────> Display login form
      │
Enter credentials:
- Username
- Password
      │
      ├──────────────────> Authenticate user
      │                    ├─ Find user by username
      │                    ├─ Verify password hash
      │                    └─ Check is_active flag
      │
Submit form                         │
      │                             │
      ├─────────────────────────────┤
      │                             │
      │                    Valid credentials?
      │                             │
      │                    ┌────────┴────────┐
      │                    │                 │
      │                   YES               NO
      │                    │                 │
      │           Create session      Show error
      │           ├─ Set cookie       message
      │           └─ Update last_login     │
      │                    │                 │
      │<───────────────────┤                 │
      │                                      │
Redirected to homepage              Stay on login page
with welcome message                with error message
      │                                      │
      ▼                                      ▼
✓ Logged in                          ✗ Try again
✓ Session active
```

## Logout Flow

```
User Action                 System Process                  Result
───────────                ────────────────               ────────

Click logout link
      │
      ├──────────────────> Display confirmation page
      │
Confirm logout
      │
      ├──────────────────> Clear session
      │                    ├─ Delete session cookie
      │                    ├─ Clear session data
      │                    └─ Invalidate token
      │
Submit confirmation                 │
      │                             │
      │<─────────────────────────────┤
      │
Redirected to homepage
with goodbye message
      │
      ▼
✓ Logged out
✓ Session cleared
```

## Profile Access Flow

```
User Action                 System Process                  Result
───────────                ────────────────               ────────

Visit /profile/
      │
      ├──────────────────> Check authentication
      │                    └─ @login_required decorator
      │
      │                    User logged in?
      │                             │
      │                    ┌────────┴────────┐
      │                    │                 │
      │                   YES               NO
      │                    │                 │
      │           Fetch user data    Redirect to login
      │           ├─ Username        with ?next=/profile/
      │           ├─ Email                  │
      │           ├─ Name                   │
      │           └─ Dates                  │
      │                    │                 │
      │<───────────────────┤                 │
      │                                      │
Display profile page              Login page shown
with user information             with redirect notice
      │                                      │
      ▼                                      ▼
✓ Profile displayed              → After login, return
                                   to /profile/
```

## Email Sending Flow

```
Trigger Event              Email Process                    Delivery
─────────────             ──────────────                  ──────────

User registers
      │
      ├──────────────────> send_welcome_email_to_user()
      │                    │
      │                    ├─ Create email subject
      │                    ├─ Render HTML template
      │                    ├─ Create plain text version
      │                    └─ Prepare email object
      │                             │
      │                    Send via EMAIL_BACKEND
      │                             │
      │                    ┌────────┴────────┐
      │                    │                 │
      │              Console Backend   SMTP Backend
      │                    │                 │
      │           Print to terminal   Send to SMTP server
      │           (Development)       (Production)
      │                    │                 │
      │<───────────────────┴─────────────────┘
      │
Email "sent"
      │
      ▼
✓ Welcome email delivered
  (check console or inbox)
```

## Password Security Flow

```
User Input                 Security Process                Storage
──────────                ────────────────               ─────────

User enters:
"mypassword123"
      │
      ├──────────────────> Django password hasher
      │                    │
      │                    ├─ Algorithm: PBKDF2
      │                    ├─ Generate random salt
      │                    ├─ 260,000 iterations
      │                    └─ SHA256 hash function
      │                             │
      │                    Create hash string:
      │                    "pbkdf2_sha256$260000$
      │                     salt$hash"
      │                             │
      │                             ▼
      │                    Store in database
      │                    ├─ Never store plain text
      │                    ├─ Hash is one-way
      │                    └─ Salt prevents rainbow tables
      │
      │
Login attempt:                     │
"mypassword123"                    │
      │                             │
      ├──────────────────────────────┤
      │                             │
      │                    Retrieve stored hash
      │                    Hash input with same salt
      │                    Compare hashes
      │                             │
      │                    Match?   │
      │                    ┌────────┴────────┐
      │                    │                 │
      │                   YES               NO
      │                    │                 │
      │<───────────────────┤                 │
      │                                      │
✓ Login successful              ✗ Login failed
                                (password incorrect)
```

## Session Management

```
Login                      Session Lifecycle               Logout
─────                     ─────────────────              ──────

User logs in
      │
      ├──────────────────> Create session
      │                    ├─ Generate session ID
      │                    ├─ Store user ID
      │                    ├─ Set expiry time
      │                    └─ Create cookie
      │                             │
      │<─────────────────────────────┤
      │
Session cookie sent
to browser
      │
      ├──────────────────> Browser stores cookie
      │
      │
Each request:                      │
      │                             │
      ├──────────────────────────────┤
      │                             │
      │                    Read session cookie
      │                    Validate session ID
      │                    Load user data
      │                    Check expiry
      │                             │
      │<─────────────────────────────┤
      │
Request processed
with user context
      │
      │
User logs out:                     │
      │                             │
      ├──────────────────────────────┤
      │                             │
      │                    Delete session
      │                    Clear cookie
      │                    Invalidate ID
      │                             │
      │<─────────────────────────────┤
      │
Session ended
```

## Form Validation Flow

```
Form Submission            Validation Process              Result
───────────────           ──────────────────             ────────

User submits form
      │
      ├──────────────────> Django form validation
      │                    │
      │                    ├─ Field-level validation
      │                    │  ├─ Required fields present?
      │                    │  ├─ Correct data types?
      │                    │  ├─ Max length respected?
      │                    │  └─ Format valid (email)?
      │                    │
      │                    ├─ Custom validators
      │                    │  ├─ Email unique?
      │                    │  ├─ Username available?
      │                    │  └─ Password strong enough?
      │                    │
      │                    └─ Form-level validation
      │                       ├─ Passwords match?
      │                       └─ CSRF token valid?
      │                             │
      │                    All valid?
      │                             │
      │                    ┌────────┴────────┐
      │                    │                 │
      │                   YES               NO
      │                    │                 │
      │           Process form       Collect errors
      │           └─ Save data       ├─ Field errors
      │                              └─ Form errors
      │                    │                 │
      │<───────────────────┴─────────────────┘
      │                             │
Success redirect              Redisplay form
with message                  with error messages
      │                             │
      ▼                             ▼
✓ Data saved                  ✗ Fix errors and resubmit
```

## URL Routing

```
Browser Request            Django URL Routing              View Function
───────────────           ──────────────────             ─────────────

GET /register/
      │
      ├──────────────────> urls.py
      │                    │
      │                    Match pattern: 'register/'
      │                    │
      │                    Route to: auth_views.register_view
      │                             │
      │                             ▼
      │                    register_view(request)
      │                    ├─ Check if authenticated
      │                    ├─ Create form
      │                    └─ Render template
      │                             │
      │<─────────────────────────────┤
      │
HTML response
(registration form)


POST /register/
      │
      ├──────────────────> urls.py
      │                    │
      │                    Match pattern: 'register/'
      │                    │
      │                    Route to: auth_views.register_view
      │                             │
      │                             ▼
      │                    register_view(request)
      │                    ├─ Validate form
      │                    ├─ Create user
      │                    ├─ Send email
      │                    ├─ Login user
      │                    └─ Redirect
      │                             │
      │<─────────────────────────────┤
      │
HTTP redirect
to homepage
```

## Integration with Existing System

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Flow                        │
└─────────────────────────────────────────────────────────────┘

Homepage (/)
      │
      ├─ Not logged in ──> Show: Login | Register
      │
      └─ Logged in ─────> Show: Welcome, [user] | Profile | Logout


Member Management (/member/create/)
      │
      ├─ Currently: Anyone can access
      │
      └─ Future: Add @login_required
                 └─> Only logged-in users can create members


User Authentication
      │
      ├─ /register/ ──> Create account
      │                 └─> Auto-login
      │                     └─> Redirect to homepage
      │
      ├─ /login/ ─────> Enter credentials
      │                 └─> Validate
      │                     └─> Create session
      │                         └─> Redirect to homepage
      │
      ├─ /logout/ ────> Confirm logout
      │                 └─> Clear session
      │                     └─> Redirect to homepage
      │
      └─ /profile/ ───> @login_required
                        └─> Show user info
                            └─> Or redirect to login


Future Integration
      │
      └─ Link User to Names model
         └─> user = OneToOneField(User)
             └─> member.user.username
                 └─> user.member_profile.firstname
```

---

These diagrams show how the authentication system works at each step. Use them as a reference when customizing or troubleshooting the system.
