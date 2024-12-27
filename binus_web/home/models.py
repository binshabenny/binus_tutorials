from django.db import models
from embed_video.fields import EmbedVideoField
import uuid

class Item(models.Model):
    title = models.CharField(max_length=100)
    video = EmbedVideoField() 
    playlist_url = models.URLField(blank=True, null=True, help_text="Enter the URL for a YouTube playlist.")
    chapter_title = models.CharField(max_length=100)

    def __str__(self):
        return self.title # same like models.URLField()

# Create your models here.
class Tutorial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    class_name = models.CharField(max_length=50)  # Consider renaming if 'class' conflicts with Python keywords
    mode_of_class = models.CharField(max_length=50, choices=[('Online', 'Online'), ('Offline', 'Offline')])
    class_timings = models.CharField(max_length=100)  # You may use DateTimeField if specific times are needed
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='class_images/')

    def __str__(self):
        return self.title
    
class Pictures(models.Model):
        title = models.CharField(max_length=100)
        image = models.ImageField(upload_to='images/')

        def __str__(self):
            return self.title
        

class BookSeat(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField(max_length=100)
     phone_number = models.CharField(max_length=15)
     place = models.CharField(max_length=100) 
     subject = models.ForeignKey(Tutorial, on_delete=models.CASCADE) 
     order_id =models.CharField(max_length=100, blank=True)
     status = models.BooleanField(default=False)
     payment_id = models.CharField(max_length=100, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"{self.name} - {self.subject}"
     

class Contact(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField(max_length=100, unique=True)
     phonenumber =models.CharField(max_length=12)
     subject =models.CharField(max_length=100)
     message = models.TextField(max_length=255)

     def __str__(self):
        return f"{self.name} - {self.subject}"