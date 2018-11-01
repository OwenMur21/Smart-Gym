from django.db import models
from ..gym.models import Gym


#Create your models here.
class Trainer(models.Model):
    name = models.CharField(max_length =30)
    bio = models.CharField(max_length =30)
    location= models.ForeignKey(location)
    gym = models.ForeignKey(Gym)
    specially=models.CharField(max_length =30)
    year_Experience=models.CharField(max_length =30)
    user = models.ForeignKey(User)

   
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
