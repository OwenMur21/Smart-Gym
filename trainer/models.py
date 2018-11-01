from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from gym.models import Gym


#Create your models here.
class Trainer(models.Model):
    name = models.CharField(max_length =30)
    bio = models.CharField(max_length =30)
    # location= models.ForeignKey(location)
    gym = models.ForeignKey(Gym)
    specially=models.CharField(max_length =30)
    year_Experience=models.CharField(max_length =30)
    user = models.OneToOneField(User)



    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Trainer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.trainer.save()

    post_save.connect(save_user_profile, sender=User)


   
    def __str__(self):
        return self.location
    def save_trainer(self):
        self.save()  

    def delete_trainer(self):
        self.delete()  

    @classmethod
    def update_trainer(cls,update):
        pass
     
    @classmethod
    def search_by_trainer(cls,name):
        trainer = Trainer.objects.filter(user__username__icontains=name)
        return trainer
    @classmethod 
    def get_by_id(cls,id):
        trainer = Trainer.objects.get(user = id)
        return trainer      
