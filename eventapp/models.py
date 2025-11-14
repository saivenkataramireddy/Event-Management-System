from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=15)
    address=models.CharField(max_length=60)
    role=models.CharField(max_length=20,default="user")
    password=models.CharField(max_length=20)

class Add_event(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=15)
    budget = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)    
    date = models.DateField(unique=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_booked = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending')  # pending / accepted / rejected
    booked_by = models.ForeignKey('Users', on_delete=models.SET_NULL, null=True, blank=True)


class Registration(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    event = models.ForeignKey(Add_event, on_delete=models.CASCADE)


class EventMedia(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to='event_videos/', blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
