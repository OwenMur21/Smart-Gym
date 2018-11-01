from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

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


    





