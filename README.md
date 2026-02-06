# Django PostgreSQL Complete Setup Guide

## Step 1: Install PostgreSQL on Windows

### 1.1 Download PostgreSQL
1. Visit https://www.postgresql.org/download/windows/
2. Click on "Download the installer"
3. Download the latest version for Windows (x86-64)

### 1.2 Run the Installer
1. Double-click the downloaded `.exe` file
2. Click "Next" on the welcome screen
3. Choose installation directory (default: `C:\Program Files\PostgreSQL\16`)
4. Select components to install:
   - ✓ PostgreSQL Server
   - ✓ pgAdmin 4
   - ✓ Stack Builder
   - ✓ Command Line Tools
5. Choose data directory (default: `C:\Program Files\PostgreSQL\16\data`)
6. **Set password for postgres superuser** (IMPORTANT: Remember this password!)
7. Set port number (default: `5432`)
8. Select locale (default: `[Default locale]`)
9. Review installation summary and click "Next"
10. Wait for installation to complete
11. Uncheck "Stack Builder" and click "Finish"

### 1.3 Verify Installation
1. Open Command Prompt or PowerShell
2. Run:
```bash
psql --version
```
3. You should see: `psql (PostgreSQL) 16.x`

### 1.4 Add PostgreSQL to PATH (if not automatically added)
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Click "Edit" → "New"
5. Add: `C:\Program Files\PostgreSQL\16\bin`
6. Click "OK" on all windows
7. Restart Command Prompt/PowerShell

## Step 2: Create PostgreSQL Database User

### 2.1 Access PostgreSQL Command Line
```bash
psql -U postgres
```
Enter the password you set during installation.

### 2.2 Create a New Database User
```sql
CREATE USER django_user WITH PASSWORD 'your_secure_password';
```

### 2.3 Grant User Privileges
```sql
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'UTC';
ALTER ROLE django_user CREATEDB;
```

### 2.4 Verify User Creation
```sql
\du
```
You should see `django_user` in the list.

## Step 3: Create PostgreSQL Database

### 3.1 Create Database (while still in psql)
```sql
CREATE DATABASE django_db OWNER django_user;
```

### 3.2 Grant All Privileges
```sql
GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;
```

### 3.3 Verify Database Creation
```sql
\l
```
You should see `django_db` in the list.

### 3.4 Exit psql
```sql
\q
```

### 3.5 Test Connection with New User
```bash
psql -U django_user -d django_db
```
Enter the password for `django_user`. If successful, you're connected!

## Step 4: Install Django PostgreSQL Driver

### 4.1 Activate Virtual Environment (if using one)
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4.2 Install psycopg2
```bash
pip install psycopg2-binary
```

### 4.3 Verify Installation
```bash
pip list | grep psycopg2
```

## Step 5: Configure Django Project

### 5.1 Locate settings.py
Navigate to your Django project directory:
```bash
cd your_project_name
```
Open `your_project_name/settings.py`

### 5.2 Update Database Configuration
Find the `DATABASES` section and replace it with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5.3 Save the File

## Step 6: Test Database Connection

### 6.1 Test Connection
```bash
python manage.py check --database default
```
If no errors appear, the connection is successful!

### 6.2 Alternative Test (Django Shell)
```bash
python manage.py shell
```
Then run:
```python
from django.db import connection
connection.ensure_connection()
print("Database connection successful!")
exit()
```

## Step 7: Create Django Models

### 7.1 Create or Update Models
In your app's `models.py` (e.g., `myapp/models.py`):

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

## Step 8: Run Django Migrations

### 8.1 Create Migration Files
```bash
python manage.py makemigrations
```
This creates migration files based on your models.

### 8.2 View SQL Before Migrating (Optional)
```bash
python manage.py sqlmigrate myapp 0001
```

### 8.3 Apply Migrations
```bash
python manage.py migrate
```
This creates all necessary tables in PostgreSQL.

### 8.4 Verify Migrations
```bash
python manage.py showmigrations
```
All migrations should have `[X]` marks.

### 8.5 Create Django Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to set username, email, and password.

## Step 9: Access Database Entries

### Method 1: Using Django ORM (Python Shell)

#### 9.1 Open Django Shell
```bash
python manage.py shell
```

#### 9.2 Import Your Models
```python
from myapp.models import Product
```

#### 9.3 Create Records
```python
# Create single record
product1 = Product.objects.create(
    name='Laptop',
    price=999.99,
    description='High-performance laptop'
)

# Create multiple records
Product.objects.bulk_create([
    Product(name='Mouse', price=25.50, description='Wireless mouse'),
    Product(name='Keyboard', price=75.00, description='Mechanical keyboard'),
])
```

#### 9.4 Read Records
```python
# Get all records
all_products = Product.objects.all()
for product in all_products:
    print(f"{product.name}: ${product.price}")

# Filter records
expensive = Product.objects.filter(price__gt=50)

# Get single record
product = Product.objects.get(id=1)
print(product.name)

# Get first/last
first = Product.objects.first()
last = Product.objects.last()

# Count records
count = Product.objects.count()
```

#### 9.5 Update Records
```python
# Update single record
product = Product.objects.get(id=1)
product.price = 899.99
product.save()

# Update multiple records
Product.objects.filter(price__lt=30).update(price=29.99)
```

#### 9.6 Delete Records
```python
# Delete single record
product = Product.objects.get(id=1)
product.delete()

# Delete multiple records
Product.objects.filter(price__lt=20).delete()

# Delete all records (use with caution!)
Product.objects.all().delete()
```

#### 9.7 Advanced Queries
```python
# Order by
products = Product.objects.order_by('-price')  # Descending
products = Product.objects.order_by('name')    # Ascending

# Limit results
products = Product.objects.all()[:5]  # First 5

# Exclude
products = Product.objects.exclude(price__lt=50)

# Complex queries
from django.db.models import Q
products = Product.objects.filter(
    Q(price__lt=100) | Q(name__icontains='laptop')
)

# Aggregate
from django.db.models import Avg, Sum, Count
avg_price = Product.objects.aggregate(Avg('price'))
total = Product.objects.aggregate(Sum('price'))
```

### Method 2: Using PostgreSQL Command Line (psql)

#### 9.1 Access Database
```bash
psql -U django_user -d django_db
```

#### 9.2 List All Tables
```sql
\dt
```

#### 9.3 View Table Structure
```sql
\d myapp_product
```

#### 9.4 SQL Queries
```sql
-- Select all records
SELECT * FROM myapp_product;

-- Select specific columns
SELECT id, name, price FROM myapp_product;

-- Filter records
SELECT * FROM myapp_product WHERE price > 50;

-- Order results
SELECT * FROM myapp_product ORDER BY price DESC;

-- Count records
SELECT COUNT(*) FROM myapp_product;

-- Average price
SELECT AVG(price) FROM myapp_product;

-- Insert record
INSERT INTO myapp_product (name, price, description, created_at)
VALUES ('Monitor', 299.99, '27-inch monitor', NOW());

-- Update record
UPDATE myapp_product SET price = 249.99 WHERE id = 1;

-- Delete record
DELETE FROM myapp_product WHERE id = 1;
```

#### 9.5 Exit psql
```sql
\q
```

### Method 3: Using Django Admin Panel

#### 9.1 Register Model in admin.py
In `myapp/admin.py`:
```python
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
```

#### 9.2 Start Development Server
```bash
python manage.py runserver
```

#### 9.3 Access Admin Panel
1. Open browser: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click on "Products" to view/edit/delete records

### Method 4: Using pgAdmin 4 (GUI)

#### 9.1 Open pgAdmin 4
1. Search "pgAdmin 4" in Windows Start Menu
2. Open the application

#### 9.2 Connect to Server
1. Expand "Servers" in left panel
2. Click on "PostgreSQL 16"
3. Enter postgres password

#### 9.3 Navigate to Database
1. Expand "Databases" → "django_db"
2. Expand "Schemas" → "public" → "Tables"
3. Right-click on table → "View/Edit Data" → "All Rows"

## Step 10: Common Database Operations

### 10.1 Backup Database
```bash
pg_dump -U django_user -d django_db -f backup.sql
```

### 10.2 Restore Database
```bash
psql -U django_user -d django_db -f backup.sql
```

### 10.3 Reset Migrations (if needed)
```bash
# Delete migration files (except __init__.py)
# Then run:
python manage.py makemigrations
python manage.py migrate
```

### 10.4 Check Database Connection
```bash
python manage.py dbshell
```

## Troubleshooting

### Connection Refused
- Verify PostgreSQL service is running: Services → postgresql-x64-16
- Check firewall settings
- Verify credentials in settings.py

### Authentication Failed
- Double-check username and password in settings.py
- Verify user exists: `psql -U postgres` then `\du`

### Database Does Not Exist
- Create database: `psql -U postgres` then `CREATE DATABASE django_db;`

### Migration Errors
```bash
python manage.py migrate --fake-initial
```

### Port Already in Use
- Change port in settings.py or stop conflicting service
