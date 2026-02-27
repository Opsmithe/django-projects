# Run These Commands - File Upload Setup

## Copy and paste these commands one by one

### 1. Activate Virtual Environment
```powershell
.\myworld\Scripts\Activate.ps1
```

### 2. Install Pillow
```powershell
pip install Pillow
```

### 3. Navigate to Project Directory
```powershell
cd project
```

### 4. Create Migration
```powershell
python manage.py makemigrations
```

### 5. Run Migration
```powershell
python manage.py migrate
```

### 6. Start Development Server
```powershell
python manage.py runserver
```

---

## Then Test in Browser

1. Open: `http://127.0.0.1:8000/members/create/`
2. Fill in the form
3. Upload a profile picture (JPG or PNG, under 5MB)
4. Click "Create Member"
5. Verify the image displays

---

## Expected Output

### After Step 2 (Install Pillow):
```
Successfully installed Pillow-10.x.x
```

### After Step 4 (Create Migration):
```
Migrations for 'club':
  club\migrations\0008_names_profile_picture.py
    - Add field profile_picture to names
```

### After Step 5 (Run Migration):
```
Operations to perform:
  Apply all migrations: admin, auth, club, contenttypes, sessions
Running migrations:
  Applying club.0008_names_profile_picture... OK
```

### After Step 6 (Start Server):
```
Starting development server at http://127.0.0.1:8000/
```

---

## Done!

The file upload feature is now ready to use.

For more information, see:
- `QUICK_START.md` - 3-minute setup guide
- `project/FILE_UPLOAD_SUMMARY.md` - What was implemented
- `project/FILE_UPLOAD_GUIDE.md` - Complete documentation
