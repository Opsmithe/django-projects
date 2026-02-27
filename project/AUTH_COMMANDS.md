# Authentication System - Command Reference

Quick reference for common commands and operations.

## Server Commands

### Start Development Server
```bash
cd project
python manage.py runserver
```

### Stop Server
Press `Ctrl+C` in terminal

---

## User Management Commands

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow prompts to enter username, email, and password.

### Create User via Shell
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Create regular user
user = User.objects.create_user(
    username='johndoe',
    email='john@example.com',
    password='securepass123',
    first_name='John',
    last_name='Doe'
)

# Create superuser
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='adminpass123'
)
```

### List All Users
```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Get all users
users = User.objects.all()
for user in users:
    print(f"{user.username} - {user.email}")

# Count users
print(f"Total users: {User.objects.count()}")
```

### Get Specific User
```python
from django.contrib.auth.models import User

# By username
user = User.objects.get(username='testuser')

# By email
user = User.objects.get(email='test@example.com')

# By ID
user = User.objects.get(id=1)

# Print user details
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Name: {user.get_full_name()}")
print(f"Joined: {user.date_joined}")
print(f"Last login: {user.last_login}")
print(f"Active: {user.is_active}")
print(f"Staff: {user.is_staff}")
print(f"Superuser: {user.is_superuser}")
```

### Update User
```python
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')

# Update fields
user.email = 'newemail@example.com'
user.first_name = 'NewFirst'
user.last_name = 'NewLast'
user.save()

# Change password
user.set_password('newpassword123')
user.save()
```

### Delete User
```python
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')
user.delete()
```

### Deactivate User (Soft Delete)
```python
from django.contrib.auth.models import User

user = User.objects.get(username='testuser')
user.is_active = False
user.save()
```

---

## Database Commands

### Make Migrations (If Models Change)
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Show Migrations
```bash
python manage.py showmigrations
```

### Reset Database (CAUTION: Deletes All Data)
```bash
# Delete database file
rm db.sqlite3

# Recreate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## Testing Commands

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test File
```bash
python manage.py test club.test_auth
```

### Run Specific Test Class
```bash
python manage.py test club.test_auth.AuthenticationTests
```

### Run Specific Test Method
```bash
python manage.py test club.test_auth.AuthenticationTests.test_login
```

### Run Tests with Verbose Output
```bash
python manage.py test --verbosity=2
```

---

## Email Testing Commands

### Test Email in Shell
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail
from django.conf import settings

# Send test email
send_mail(
    subject='Test Email',
    message='This is a test email.',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=['test@example.com'],
    fail_silently=False,
)
```

### Test Welcome Email
```python
from django.contrib.auth.models import User
from club.emails import send_welcome_email_to_user

user = User.objects.get(username='testuser')
send_welcome_email_to_user(user)
```

---

## Django Shell Commands

### Open Shell
```bash
python manage.py shell
```

### Common Shell Operations

```python
# Import models
from django.contrib.auth.models import User
from club.models import Names

# Authentication
from django.contrib.auth import authenticate

# Test authentication
user = authenticate(username='testuser', password='testpass123')
if user:
    print("Authentication successful!")
else:
    print("Authentication failed!")

# Check password
user = User.objects.get(username='testuser')
if user.check_password('testpass123'):
    print("Password correct!")

# Get user permissions
print(user.get_all_permissions())
print(user.has_perm('club.add_names'))

# Exit shell
exit()
```

---

## Admin Interface Commands

### Access Admin
1. Create superuser (if not exists):
   ```bash
   python manage.py createsuperuser
   ```

2. Start server:
   ```bash
   python manage.py runserver
   ```

3. Visit: `http://localhost:8000/admin/`

4. Login with superuser credentials

### Admin Operations
- View all users: Users → Users
- Edit user: Click username
- Delete user: Select user → Actions → Delete
- Change password: User detail → Change password
- Add user: Users → Add user

---

## Static Files Commands

### Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Clear Static Files
```bash
python manage.py collectstatic --clear --noinput
```

---

## Security Commands

### Check Security Settings
```bash
python manage.py check --deploy
```

### Change Secret Key
```python
# In settings.py, generate new key:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Debugging Commands

### Check Installed Apps
```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.INSTALLED_APPS)
```

### Check Middleware
```python
from django.conf import settings
print(settings.MIDDLEWARE)
```

### Check Database Connection
```python
from django.db import connection
print(connection.settings_dict)
```

### Check Email Settings
```python
from django.conf import settings
print(f"Backend: {settings.EMAIL_BACKEND}")
print(f"Host: {settings.EMAIL_HOST}")
print(f"Port: {settings.EMAIL_PORT}")
print(f"From: {settings.DEFAULT_FROM_EMAIL}")
```

---

## URL Commands

### Show All URLs
```bash
python manage.py shell
```

```python
from django.urls import get_resolver
resolver = get_resolver()
for pattern in resolver.url_patterns:
    print(pattern)
```

### Test URL Reverse
```python
from django.urls import reverse

print(reverse('club:register'))  # /register/
print(reverse('club:login'))     # /login/
print(reverse('club:profile'))   # /profile/
```

---

## Performance Commands

### Show SQL Queries
```bash
python manage.py shell
```

```python
from django.db import connection
from django.contrib.auth.models import User

# Enable query logging
from django.conf import settings
settings.DEBUG = True

# Perform operation
users = User.objects.all()
for user in users:
    print(user.username)

# Show queries
for query in connection.queries:
    print(query['sql'])
```

---

## Backup Commands

### Backup Database
```bash
# SQLite
cp db.sqlite3 db.sqlite3.backup

# With timestamp
cp db.sqlite3 "db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)"
```

### Restore Database
```bash
cp db.sqlite3.backup db.sqlite3
```

### Export Users to JSON
```bash
python manage.py dumpdata auth.User --indent=2 > users_backup.json
```

### Import Users from JSON
```bash
python manage.py loaddata users_backup.json
```

---

## Development Workflow

### Typical Development Session
```bash
# 1. Start server
python manage.py runserver

# 2. Make changes to code

# 3. If models changed:
python manage.py makemigrations
python manage.py migrate

# 4. Test changes in browser

# 5. Run tests
python manage.py test

# 6. Check for issues
python manage.py check

# 7. Commit changes
git add .
git commit -m "Add authentication system"
```

---

## Production Deployment

### Pre-Deployment Checklist
```bash
# 1. Check security
python manage.py check --deploy

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Test email
python manage.py shell
# ... test email sending ...
```

---

## Troubleshooting Commands

### Clear Sessions
```bash
python manage.py clearsessions
```

### Clear Cache (if using cache)
```bash
python manage.py shell
```

```python
from django.core.cache import cache
cache.clear()
```

### Reset Migrations (CAUTION)
```bash
# Delete migration files (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Delete database
rm db.sqlite3

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                  QUICK COMMAND REFERENCE                 │
├─────────────────────────────────────────────────────────┤
│ Start server:        python manage.py runserver         │
│ Create superuser:    python manage.py createsuperuser   │
│ Open shell:          python manage.py shell             │
│ Run tests:           python manage.py test              │
│ Make migrations:     python manage.py makemigrations    │
│ Apply migrations:    python manage.py migrate           │
│ Collect static:      python manage.py collectstatic     │
│ Security check:      python manage.py check --deploy    │
│ Clear sessions:      python manage.py clearsessions     │
├─────────────────────────────────────────────────────────┤
│ Admin URL:           http://localhost:8000/admin/       │
│ Register URL:        http://localhost:8000/register/    │
│ Login URL:           http://localhost:8000/login/       │
│ Profile URL:         http://localhost:8000/profile/     │
└─────────────────────────────────────────────────────────┘
```

---

## Environment Variables (Production)

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Load in settings.py:
```python
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

---

**Need more help?** Check the other documentation files:
- `AUTH_QUICKSTART.md` - Quick start guide
- `AUTHENTICATION_GUIDE.md` - Complete guide
- `AUTH_TESTING.md` - Testing instructions
- `AUTHENTICATION_FLOW.md` - System diagrams
