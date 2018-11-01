from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from client.models import Trainee


# Create your models here.
class GymManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gym_manager')
    bio = models.TextField(max_length=100, blank=True)
    profilepic = models.ImageField(upload_to='picture/',blank=True)
    
class Gym(models.Model):
  '''
  Class that contains gym class properties,methods and functions
  '''
  name = models.CharField(max_length=100)
  posted_on = models.DateTimeField(auto_now_add=True) 
  description = models.TextField(blank=True,null=True)
  image = models.ImageField(upload_to='images/')
  location = models.CharField(max_length=100)
  working_hours = models.TextField()
  manager = models.ForeignKey('GymManager',default = 0)

  class Meta:
    ordering = ['posted_on']
  

  def save_gym(self):
    self.save()

  def update_gym(self):
    self.update()

  def delete_gym(self):
    self.delete()

  @classmethod
  def get_all_gyms(cls):
    gyms = Gym.objects.all()
    return gyms

  def __str__(self):
    return self.name



class Event(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(max_length=100)
    event_date = models.DateTimeField()
    from_gym = models.ForeignKey(Gym,blank = True)
    from_client = models.ForeignKey(Trainee, blank = True)

