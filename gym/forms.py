from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gym,Image

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class GymForm(forms.ModelForm):
  '''
  Form class that enables gym admins register their gyms
  '''
  class Meta:
    model = Gym
    fields = ['name','image','location','description','working_hours',]
    exclude = ['posted_on']

class ImagesForm(forms.ModelForm):
  '''
  Form class that enables gym admins add images to gym gallery
  '''
  class Meta:
    model = Image
    fields = ['name','image',]