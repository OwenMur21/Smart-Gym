from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
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

  class Meta:
    ordering = ['posted_on']
  

  def save_gym(self):
    self.save

  def update_gym(self):
    self.update

  def delete_gym(self):
    self.delete

  @classmethod
  def get_all_gyms(cls):
    gyms = Gym.objects.all()
    return gyms

  def __str__(self):
    return self.name

