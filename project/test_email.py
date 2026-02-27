"""
Quick email test script
Run this to test if emails are working
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from club.models import Names
from club.emails import send_welcome_email

print("=" * 60)
print("EMAIL TEST SCRIPT")
print("=" * 60)

# Check email backend configuration
from django.conf import settings
print(f"\n1. Email Backend: {settings.EMAIL_BACKEND}")
print(f"2. Default From Email: {settings.DEFAULT_FROM_EMAIL}")

# Get the most recent member
try:
    member = Names.objects.latest('date_joined')
    print(f"\n3. Testing with member: {member.firstname} {member.lastname}")
    print(f"   Email: {member.email}")
    
    # Try to send email
    print("\n4. Attempting to send email...")
    result = send_welcome_email(member)
    
    if result:
        print("   ✅ Email sent successfully!")
        print("\n5. Check the output above for the email content.")
    else:
        print("   ❌ Email failed to send!")
        print("   Check the error messages above.")
        
except Names.DoesNotExist:
    print("\n❌ No members found in database!")
    print("   Create a member first, then run this test.")
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
