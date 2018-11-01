from django import forms
from .models import *


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chatroom
        exclude = ['admin']


class ChatPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['chatroom','poster','gym']