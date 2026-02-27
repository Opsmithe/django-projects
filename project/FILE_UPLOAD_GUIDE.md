# File Upload Feature - Complete Implementation Guide

## Overview

The Tennis Club application now supports profile picture uploads for members with comprehensive validation, optimization, and display features.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Configuration](#configuration)
5. [Implementation Details](#implementation-details)
6. [Usage Guide](#usage-guide)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Features

### ✅ Implemented Features

1. **Profile Picture Upload**
   - Members can upload profile pictures
   - Supports JPG, PNG, GIF, WEBP formats
   - Maximum file size: 5MB

2. **Image Validation**
   - File size validation
   - File format validation
   - Actual image verification (not just extension)

3. **Image Optimization**
   - Automatic resizing (max 800x800px)
   - Compression to reduce file size
   - Maintains aspect ratio

4. **File Organization**
   - Files stored in organized folders per member
   - Unique filenames to prevent conflicts
   - Path: `media/profile_pics/member-slug/filename.jpg`

5. **Display Features**
   - Large profile picture on detail page
   - Thumbnails on member list
   - Default avatar for members without photos

6. **File Management**
   - Old pictures deleted when uploading new ones
   - Clearable file input (can remove picture)
   - Proper cleanup on member deletion

---

## Architecture

### Data Flow

```
User uploads file
    ↓
Browser sends multipart/form-data
    ↓
Django receives file in request.FILES
    ↓
Form validation (size, format)
    ↓
File saved to media/profile_pics/
    ↓
Image optimized (resize, compress)
    ↓
Path stored in database
    ↓
Image displayed in templates
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    File Upload System                    │
└─────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Settings   │ ───> │  URL Config  │ ───> │  File Utils  │
│  (config)    │      │  (routing)   │      │  (helpers)   │
└──────────────┘      └──────────────┘      └──────────────┘
       │                      │                      │
       v                      v                      v
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Model     │ ───> │     Form     │ ───> │     View     │
│ (database)   │      │ (validation) │      │  (logic)     │
└──────────────┘      └──────────────┘      └──────────────┘
       │                      │                      │
       v                      v                      v
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Template   │ ───> │     CSS      │ ───> │  JavaScript  │
│  (display)   │      │  (styling)   │      │  (preview)   │
└──────────────┘      └──────────────┘      └──────────────┘
```

---

## File Structure

### Directory Layout

```
project/
├── media/                          # User uploaded files (NEW)
│   └── profile_pics/               # Profile pictures directory
│       ├── john-doe/               # Per-member folders
│       │   └── abc123_photo.jpg
│       └── jane-smith/
│           └── def456_photo.jpg
│
├── club/
│   ├── static/club/
│   │   ├── css/
│   │   │   └── style.css           # Updated with image styles
│   │   └── images/
│   │       └── default_avatar.svg  # Default avatar (NEW)
│   │
│   ├── templates/
│   │   ├── create_member.html      # Updated with enctype
│   │   ├── edit_member.html        # Updated with enctype
│   │   ├── details.html            # Shows profile picture
│   │   └── first.html              # Shows thumbnails
│   │
│   ├── file_utils.py               # File handling utilities (NEW)
│   ├── forms.py                    # Updated with file field
│   ├── models.py                   # Updated with ImageField
│   └── views.py                    # Updated with request.FILES
│
└── project/
    ├── settings.py                 # Media configuration (NEW)
    └── urls.py                     # Media URL routing (NEW)
```

---

## Configuration

### 1. Settings Configuration

**Location:** `project/settings.py`

```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
```

**Explanation:**
- `MEDIA_URL`: URL prefix for accessing uploaded files
- `MEDIA_ROOT`: Filesystem path where files are stored
- `FILE_UPLOAD_MAX_MEMORY_SIZE`: Maximum file size in bytes
- `ALLOWED_IMAGE_EXTENSIONS`: Permitted file formats

### 2. URL Configuration

**Location:** `project/urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Explanation:**
- Only serves media files in development (`DEBUG=True`)
- In production, web server (Nginx/Apache) should serve media files
- `static()` helper creates URL patterns for media files

---

## Implementation Details

### 1. File Utils Module (`club/file_utils.py`)

#### Function: `member_profile_picture_path()`

**Purpose:** Generate custom file path for uploads

**Code:**
```python
def member_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    return os.path.join(
        'profile_pics',
        instance.slug if instance.slug else 'temp',
        unique_filename
    )
```

**How it works:**
1. Extracts file extension from original filename
2. Generates unique filename using UUID
3. Creates path: `profile_pics/member-slug/unique_filename.ext`

**Example:**
```
Input: filename="photo.jpg", member.slug="john-doe"
Output: "profile_pics/john-doe/a1b2c3d4_photo.jpg"
```

#### Function: `validate_image_file()`

**Purpose:** Validate uploaded image

**Checks:**
1. File size (max 5MB)
2. File extension (jpg, png, gif, webp)
3. File is actually an image (using PIL)

**Code:**
```python
def validate_image_file(file):
    # Check size
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('File too large')
    
    # Check extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        raise ValidationError('Invalid file type')
    
    # Verify it's an image
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except:
        raise ValidationError('Invalid image file')
```

#### Function: `optimize_uploaded_image()`

**Purpose:** Optimize image after upload

**Process:**
1. Opens image with PIL
2. Converts RGBA to RGB if needed
3. Resizes to max 800x800px (maintains aspect ratio)
4. Compresses with quality=85
5. Saves optimized version

**Benefits:**
- Reduces file size (faster loading)
- Standardizes dimensions
- Saves server storage

### 2. Model Changes (`club/models.py`)

#### ImageField Addition

```python
profile_picture = models.ImageField(
    upload_to=member_profile_picture_path,
    validators=[validate_image_file],
    blank=True,
    null=True,
    help_text='Upload a profile picture (JPG, PNG, GIF, WEBP - Max 5MB)'
)
```

**Parameters:**
- `upload_to`: Function that determines file path
- `validators`: List of validation functions
- `blank=True`: Optional in forms
- `null=True`: Can be NULL in database
- `help_text`: Help text for forms

#### Helper Method

```python
def get_profile_picture_url(self):
    if self.profile_picture and hasattr(self.profile_picture, 'url'):
        return self.profile_picture.url
    return '/static/club/images/default_avatar.svg'
```

**Purpose:** Get profile picture URL with fallback to default avatar

### 3. Form Changes (`club/forms.py`)

#### ImageField Addition

```python
profile_picture = forms.ImageField(
    required=False,
    label='Profile Picture',
    widget=forms.ClearableFileInput(attrs={
        'class': 'form-file-input',
        'accept': 'image/*',
    }),
    help_text='Upload a profile picture (JPG, PNG, GIF, WEBP - Max 5MB)',
)
```

**Widget:** `ClearableFileInput`
- Renders file input
- Shows current file if exists
- Adds checkbox to clear file

**Attributes:**
- `accept="image/*"`: Browser only shows image files
- `class`: CSS styling

#### Custom Validation

```python
def clean_profile_picture(self):
    profile_picture = self.cleaned_data.get('profile_picture')
    if profile_picture:
        validate_image_file(profile_picture)
    return profile_picture
```

### 4. View Changes (`club/views.py`)

#### Key Change: `request.FILES`

**Before:**
```python
form = MemberForm(request.POST)
```

**After:**
```python
form = MemberForm(request.POST, request.FILES)
```

**Why:** `request.FILES` contains uploaded files. Without it, files won't be processed.

#### Old File Deletion

```python
if 'profile_picture' in request.FILES:
    delete_old_profile_picture(member)
```

**Purpose:** Delete old profile picture when uploading new one

### 5. Template Changes

#### Form Enctype

**Critical Addition:**
```html
<form method="POST" enctype="multipart/form-data">
```

**Why:** `enctype="multipart/form-data"` is REQUIRED for file uploads. Without it, files won't be sent to server.

#### Image Display

**Detail Page:**
```html
<img src="{{ mymember.get_profile_picture_url }}" 
     alt="{{ mymember.firstname }} {{ mymember.lastname }}" 
     class="profile-picture-large">
```

**Member List:**
```html
<img src="{{ member.get_profile_picture_url }}" 
     alt="{{ member.firstname }}"
     class="profile-picture-thumbnail">
```

---

## Usage Guide

### For Users

#### Uploading Profile Picture

1. Go to Create Member or Edit Member page
2. Click "Choose File" button
3. Select image (JPG, PNG, GIF, WEBP)
4. Image must be under 5MB
5. Click "Create Member" or "Update Member"
6. Image is automatically optimized and saved

#### Removing Profile Picture

1. Go to Edit Member page
2. Check "Clear" checkbox next to current image
3. Click "Update Member"
4. Profile picture is removed, default avatar shown

### For Developers

#### Creating Migration

```bash
cd project
python manage.py makemigrations
python manage.py migrate
```

#### Installing Pillow

```bash
pip install Pillow
```

**Why:** Django's `ImageField` requires Pillow for image processing.

#### Accessing Uploaded Files

**In Python:**
```python
member = Names.objects.get(id=1)
if member.profile_picture:
    print(member.profile_picture.url)  # URL
    print(member.profile_picture.path)  # Filesystem path
    print(member.profile_picture.size)  # File size
```

**In Templates:**
```django
{{ member.profile_picture.url }}
{{ member.profile_picture.name }}
{{ member.profile_picture.size }}
```

---

## Testing

### Manual Testing

#### Test 1: Upload Valid Image

**Steps:**
1. Create new member
2. Upload JPG image (< 5MB)
3. Submit form

**Expected:**
- ✅ Form submits successfully
- ✅ Image appears on detail page
- ✅ Thumbnail appears on member list
- ✅ File saved in `media/profile_pics/member-slug/`

#### Test 2: Upload Invalid File

**Steps:**
1. Try uploading PDF file
2. Submit form

**Expected:**
- ❌ Form shows error: "File type not allowed"
- ❌ Form doesn't submit

#### Test 3: Upload Large File

**Steps:**
1. Try uploading 10MB image
2. Submit form

**Expected:**
- ❌ Form shows error: "File size must be under 5MB"
- ❌ Form doesn't submit

#### Test 4: Update Profile Picture

**Steps:**
1. Edit existing member
2. Upload new image
3. Submit form

**Expected:**
- ✅ Old image deleted
- ✅ New image saved
- ✅ New image displayed

#### Test 5: Remove Profile Picture

**Steps:**
1. Edit member with profile picture
2. Check "Clear" checkbox
3. Submit form

**Expected:**
- ✅ Profile picture removed
- ✅ Default avatar shown
- ✅ File deleted from server

### Automated Testing

```python
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from club.models import Names

class ProfilePictureTests(TestCase):
    def test_upload_valid_image(self):
        # Create test image
        image = SimpleUploadedFile(
            "test.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        # Create member with image
        member = Names.objects.create(
            firstname="Test",
            lastname="User",
            profile_picture=image
        )
        
        # Assert image was saved
        self.assertTrue(member.profile_picture)
        self.assertIn('profile_pics', member.profile_picture.name)
```

---

## Troubleshooting

### Issue 1: Images Not Uploading

**Symptoms:**
- Form submits but no image saved
- `profile_picture` field is None

**Solutions:**

**A. Check form enctype**
```html
<!-- ❌ WRONG -->
<form method="POST">

<!-- ✅ CORRECT -->
<form method="POST" enctype="multipart/form-data">
```

**B. Check view includes request.FILES**
```python
# ❌ WRONG
form = MemberForm(request.POST)

# ✅ CORRECT
form = MemberForm(request.POST, request.FILES)
```

### Issue 2: Images Not Displaying

**Symptoms:**
- Image uploaded but broken image icon shown
- 404 error for image URL

**Solutions:**

**A. Check media URL configuration**
```python
# In settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**B. Check URL configuration**
```python
# In urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**C. Check file exists**
```bash
ls media/profile_pics/
```

### Issue 3: Pillow Not Installed

**Symptoms:**
- Error: "Cannot use ImageField because Pillow is not installed"

**Solution:**
```bash
pip install Pillow
```

### Issue 4: Permission Denied

**Symptoms:**
- Error: "Permission denied" when saving file

**Solution:**
```bash
# Linux/Mac
chmod 755 media/
chmod 755 media/profile_pics/

# Windows
# Check folder permissions in Properties
```

### Issue 5: File Too Large

**Symptoms:**
- Large files fail to upload
- No error message

**Solution:**

**A. Check Django setting**
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

**B. Check web server limits (production)**
```nginx
# Nginx
client_max_body_size 5M;
```

---

## Production Deployment

### 1. Configure Web Server

**Nginx Example:**
```nginx
location /media/ {
    alias /path/to/project/media/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 2. Collect Static Files

```bash
python manage.py collectstatic
```

### 3. Set Permissions

```bash
chmod 755 media/
chown www-data:www-data media/
```

### 4. Use Cloud Storage (Optional)

For scalability, consider using:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

**Install django-storages:**
```bash
pip install django-storages boto3
```

**Configure:**
```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
```

---

## Summary

✅ **Profile picture upload implemented**
✅ **Image validation (size, format)**
✅ **Automatic optimization (resize, compress)**
✅ **Organized file storage**
✅ **Display on detail and list pages**
✅ **Default avatar fallback**
✅ **Old file cleanup**
✅ **Comprehensive documentation**

The file upload feature is production-ready and follows Django best practices!
