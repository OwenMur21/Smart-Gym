from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gym.models import Gym
from client.models import Trainee


class Event(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(max_length=100)
    event_date = models.DateTimeField()
    from_gym = models.ForeignKey(Gym,blank = True)
    from_client = models.ForeignKey(Trainee, blank = True)


class Chatroom(models.Model):
    name = models.CharField(max_length=20,unique=True)
    info = models.TextField(max_length=100)
    admin = models.ForeignKey(User,related_name='administrate')

    def save_chatroom(self):
        self.save()

    def remove_chatroom(self):
        self.delete()

    @classmethod
    def get_chatroom(cls,id):
        room = Chatroom.objects.get(id=id)
        return room


class Post(models.Model):
    title = models.CharField(max_length=30)
    post = models.TextField(max_length=100)
    chatroom = models.ForeignKey(Chatroom,related_name='posts',null=True)
    poster = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')


    def save_post(self):
        self.save()

    def remove_post(self):
        self.delete()

    @classmethod
    def get_hood_posts(cls,id):
        posts = Post.objects.filter(id = id)
        return posts