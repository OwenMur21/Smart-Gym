from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from  gym.models import Gym
from .models import Chatroom


class Trainee(models.Model):
    """
    Class that contains Profile details
    """
    name = models.CharField(max_length = 30)
    profile_pic = models.ImageField(upload_to = 'images/', blank=True)
    goals = (
    ('Losing weight', 'Losing weight'),
    ('Getting toned', 'Getting toned'),
    ('Getting bigger', 'Getting bigger'),
    ('Maintain fitness', 'Maintain fitness'),
    )
    weight = models.CharField(max_length = 10)
    height = models.CharField(max_length = 10)
    goal = models.CharField(max_length = 30, choices=goals)
    contact = models.CharField(max_length = 30, blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    chatroom = models.ManyToManyField(Chatroom)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Trainee.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.trainee.save()

    post_save.connect(save_user_profile, sender=User)



    def __str__(self):
        return self.name

    def save_trainee(self):
        self.save()

    def delete_trainee(self):
        self.delete()


    @classmethod
    def addchatroom(cls,user,newroom):
        room, created = cls.objects.get_or_create(
            user = user
        )
        room.chatroom.add(newroom)

    @classmethod
    def removechatroom(cls, user, newroom):
        room, created = cls.objects.get_or_create(
            user=user
        )
        room.chatroom.remove(newroom)



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



