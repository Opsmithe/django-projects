from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from .file_utils import member_profile_picture_path, validate_image_file
# if using db_default --> from django.db.models.functions import Now()

# Create your models here.
class Names(models.Model):
   class Status(models.TextChoices):
      """a status class to set choices for players"""
      NOT_PLAYED = "NPL", "Not_Played"
      PLAYED = "PL", "Played"

   firstname = models.CharField(max_length=250, default='Unknown')
   lastname = models.CharField(max_length=250, default='Member')
   phoneNumber = models.CharField(max_length=15, default='000-000-0000')
   email = models.EmailField(unique=True, blank=True, null=True)
   slug = models.SlugField(max_length=500, unique=True, blank=True)
   city = models.CharField(max_length=250, default='Not specified')
   location = models.CharField(max_length=250, default='Not specified')
   date_joined = models.DateField(auto_now_add=True) #(auto_now_add=True) adds the date when an object is created
   date_updated = models.DateField(null=True) # (auto_now=True) updates the date when object is updated
   date_started = models.DateField(default=timezone.now) #(db_default=Now()) uses db computed value for the date, same purpose as doing the (default=timezone.now)
   status = models.CharField(
      max_length=4,
      choices=Status,
      default=Status.NOT_PLAYED
   )
   
   # Profile picture field
   # ImageField: Django field for image uploads
   # upload_to: function that determines where file is saved
   # validators: list of validation functions to run
   # blank=True: field is optional in forms
   # null=True: database allows NULL values
   # help_text: displayed in forms to guide users
   profile_picture = models.ImageField(
       upload_to=member_profile_picture_path,
       validators=[validate_image_file],
       blank=True,
       null=True,
       help_text='Upload a profile picture (JPG, PNG, GIF, WEBP - Max 5MB)'
   )

# a metadata class of the Names class used to order the arrangement and sort
   class Metadata:
      """
      metadata class of the Names class used for ordering
      """
      ordering = ['-date_joined']
      # defining a db index to help with query filter
      



   def __str__(self):
      return f"{self.firstname} {self.lastname}" 
   
   def save(self, *args, **kwargs):
      # Generate unique email if not provided
      if not self.email:
         base_email = f"{self.firstname.lower()}.{self.lastname.lower()}@example.com"
         email = base_email
         counter = 1
         # Ensure email is unique
         while Names.objects.filter(email=email).exclude(pk=self.pk).exists():
            email = f"{self.firstname.lower()}.{self.lastname.lower()}{counter}@example.com"
            counter += 1
         self.email = email
      
      # Generate unique slug if not provided
      if not self.slug:
         self.slug = slugify(f"{self.firstname}-{self.lastname}-{self.city}")
      
      # Save the instance first
      super().save(*args, **kwargs)
      
      # Optimize profile picture after saving (if exists)
      if self.profile_picture:
         from .file_utils import optimize_uploaded_image
         try:
            optimize_uploaded_image(self.profile_picture.path)
         except Exception as e:
            print(f"Error optimizing image: {e}")
   
   def get_absolute_url(self):
      return reverse('club:member-detail', kwargs={'slug': self.slug})
   
   def get_profile_picture_url(self):
      """
      Get the URL for the member's profile picture.
      
      Returns the URL to the uploaded profile picture if it exists,
      otherwise returns the URL to the default avatar.
      
      Returns:
          str: URL to profile picture or default avatar
          
      Example:
          >>> member = Names.objects.get(id=1)
          >>> member.get_profile_picture_url()
          '/media/profile_pics/john-doe/photo.jpg'
      """
      if self.profile_picture and hasattr(self.profile_picture, 'url'):
         return self.profile_picture.url
      
      # Return path to default avatar
      return '/static/club/images/default_avatar.svg'
