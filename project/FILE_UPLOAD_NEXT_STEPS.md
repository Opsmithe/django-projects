# File Upload Feature - Next Steps

## Current Status

✅ **Completed:**
- Media files configuration in `settings.py`
- URL routing for media files in `urls.py`
- File utility functions in `club/file_utils.py`
- Profile picture field added to `Names` model
- Form updated with profile picture field and validation
- Views updated to handle file uploads (`request.FILES`)
- Templates updated with `enctype="multipart/form-data"`
- Default avatar SVG created
- CSS styles for profile pictures added
- Comprehensive documentation created

❌ **Pending:**
- Install Pillow library
- Create and run database migration
- Test file upload functionality

---

## Step-by-Step Instructions

### Step 1: Activate Virtual Environment

```powershell
# Navigate to project root
cd C:\Users\USER-PC\DJANGO

# Activate virtual environment
.\myworld\Scripts\Activate.ps1
```

**Expected Output:**
```
(myworld) PS C:\Users\USER-PC\DJANGO>
```

---

### Step 2: Install Pillow

```powershell
pip install Pillow
```

**What is Pillow?**
- Pillow is a Python imaging library
- Required by Django's `ImageField` for image processing
- Handles image validation, resizing, and optimization

**Expected Output:**
```
Collecting Pillow
  Downloading Pillow-10.x.x-cp312-cp312-win_amd64.whl
Installing collected packages: Pillow
Successfully installed Pillow-10.x.x
```

**Verify Installation:**
```powershell
python -c "import PIL; print(f'Pillow version: {PIL.__version__}')"
```

---

### Step 3: Create Migration

```powershell
cd project
python manage.py makemigrations
```

**What This Does:**
- Detects changes in `models.py` (new `profile_picture` field)
- Creates a migration file in `club/migrations/`
- Migration file contains instructions to add field to database

**Expected Output:**
```
Migrations for 'club':
  club\migrations\0008_names_profile_picture.py
    - Add field profile_picture to names
```

**What Gets Created:**
- New file: `project/club/migrations/0008_names_profile_picture.py`
- This file contains SQL instructions to alter the database table

---

### Step 4: Run Migration

```powershell
python manage.py migrate
```

**What This Does:**
- Executes the migration file
- Adds `profile_picture` column to `club_names` table in database
- Updates database schema

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, club, contenttypes, sessions
Running migrations:
  Applying club.0008_names_profile_picture... OK
```

**Database Changes:**
```sql
-- SQL executed by Django:
ALTER TABLE club_names ADD COLUMN profile_picture VARCHAR(100) NULL;
```

---

### Step 5: Create Media Directory

```powershell
# Still in project directory
New-Item -ItemType Directory -Path "media" -Force
New-Item -ItemType Directory -Path "media\profile_pics" -Force
```

**What This Does:**
- Creates `media/` folder for uploaded files
- Creates `media/profile_pics/` subfolder for profile pictures

**Expected Output:**
```
    Directory: C:\Users\USER-PC\DJANGO\project

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        2/27/2026   3:00 PM                media
d-----        2/27/2026   3:00 PM                profile_pics
```

---

### Step 6: Start Development Server

```powershell
python manage.py runserver
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 27, 2026 - 15:00:00
Django version 6.0.1, using settings 'project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

### Step 7: Test File Upload

#### Test 1: Create New Member with Profile Picture

1. Open browser: `http://127.0.0.1:8000/members/create/`
2. Fill in form:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@example.com
   - Phone: 123-456-7890
   - City: New York
   - Location: Manhattan
   - Status: Played
   - Profile Picture: Choose a JPG/PNG file (< 5MB)
3. Click "Create Member"

**Expected Result:**
- ✅ Success message displayed
- ✅ Redirected to member detail page
- ✅ Profile picture displayed on detail page
- ✅ File saved in `media/profile_pics/john-doe/`
- ✅ Image optimized (resized to max 800x800px)

#### Test 2: View Member List

1. Go to: `http://127.0.0.1:8000/members/`
2. Check member list

**Expected Result:**
- ✅ Profile picture thumbnail displayed next to member name
- ✅ Default avatar shown for members without pictures

#### Test 3: Edit Member - Update Picture

1. Click "Edit" on a member
2. Upload new profile picture
3. Click "Update Member"

**Expected Result:**
- ✅ Old picture deleted from server
- ✅ New picture saved and displayed
- ✅ File saved in member's folder

#### Test 4: Edit Member - Remove Picture

1. Click "Edit" on a member with picture
2. Check "Clear" checkbox next to current picture
3. Click "Update Member"

**Expected Result:**
- ✅ Picture removed from database
- ✅ File deleted from server
- ✅ Default avatar displayed

#### Test 5: Validation - Invalid File Type

1. Try uploading a PDF or TXT file
2. Submit form

**Expected Result:**
- ❌ Form shows error: "File type not allowed"
- ❌ Form doesn't submit

#### Test 6: Validation - File Too Large

1. Try uploading image > 5MB
2. Submit form

**Expected Result:**
- ❌ Form shows error: "File size must be under 5MB"
- ❌ Form doesn't submit

---

## Verification Checklist

After completing all steps, verify:

- [ ] Pillow installed successfully
- [ ] Migration created (0008_names_profile_picture.py exists)
- [ ] Migration applied (no pending migrations)
- [ ] Media directory created
- [ ] Can upload profile picture
- [ ] Picture displays on detail page
- [ ] Thumbnail displays on member list
- [ ] Can update profile picture
- [ ] Can remove profile picture
- [ ] Default avatar shows when no picture
- [ ] File size validation works
- [ ] File type validation works
- [ ] Images are optimized (check file size)

---

## File Structure After Setup

```
project/
├── media/                          # Created in Step 5
│   └── profile_pics/               # Created automatically
│       ├── john-doe/               # Created per member
│       │   └── abc123_photo.jpg    # Uploaded file
│       └── jane-smith/
│           └── def456_photo.jpg
│
├── club/
│   ├── migrations/
│   │   └── 0008_names_profile_picture.py  # Created in Step 3
│   ├── static/club/
│   │   └── images/
│   │       └── default_avatar.svg  # Already exists
│   └── ...
│
└── ...
```

---

## Troubleshooting

### Issue: "No module named 'PIL'"

**Solution:**
```powershell
pip install Pillow
```

### Issue: "No changes detected" when running makemigrations

**Solution:**
1. Check `models.py` has `profile_picture` field
2. Check imports at top of `models.py`
3. Try: `python manage.py makemigrations club`

### Issue: Images not uploading

**Check:**
1. Form has `enctype="multipart/form-data"`
2. View includes `request.FILES`
3. Media directory exists and is writable

### Issue: Images not displaying

**Check:**
1. `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`
2. URL configuration in `urls.py`
3. File exists in `media/profile_pics/`

### Issue: "Permission denied" when saving file

**Solution (Windows):**
1. Right-click `media` folder
2. Properties → Security
3. Ensure your user has "Write" permission

---

## Production Deployment Notes

When deploying to production:

1. **Web Server Configuration**
   - Configure Nginx/Apache to serve media files
   - Don't rely on Django to serve media files

2. **File Permissions**
   ```bash
   chmod 755 media/
   chown www-data:www-data media/
   ```

3. **Cloud Storage (Optional)**
   - Consider AWS S3, Google Cloud Storage, or Azure Blob
   - Install `django-storages` for cloud integration

4. **Backup Strategy**
   - Include `media/` folder in backups
   - Separate media backups from database backups

---

## Summary

The file upload feature is fully implemented and ready for testing. Follow the steps above to:

1. Install Pillow
2. Create and run migration
3. Test upload functionality

All code is in place and documented. The feature includes:
- Image validation (size, format)
- Automatic optimization (resize, compress)
- Organized file storage
- Default avatar fallback
- Old file cleanup

Once you complete these steps, the file upload feature will be fully operational!
