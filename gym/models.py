from django.db import models
import datetime as dt
from django.contrib.auth.models import User


# Create your models here.
class GymManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gym_manager')
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/',blank=True)
    



class Gym(models.Model):
    name = models.CharField(max_length = 30)
    location = models.CharField(max_length = 30)
    manager = models.ForeignKey('GymManager')







