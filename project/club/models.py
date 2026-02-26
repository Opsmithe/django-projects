from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
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
      
      super().save(*args, **kwargs)
   
   def get_absolute_url(self):
      return reverse('club:member-detail', kwargs={'slug': self.slug}) 
   