from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login, authenticate
import json
import urllib
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from django.contrib import messages
from .forms import 
from .models import *
from .decorators import check_recaptcha

@login_required(login_url='/accounts/login/')
def chatroom(request,room_id):
    current_user = request.user
    form = ChatPostForm()

    chatroom = get_object_or_404(Chatroom,pk=room_id)
    chatrooms = request.user.profile.chatroom.all()
    print(chatroom)
    posts = Post.objects.filter(chatroom=chatroom)
    if chatroom in chatrooms:
        r = chatroom
        return render(request, 'chatroom.html', {'chatroom': r,'form':form})


def post(request, id):
    chatroom = Chatroom.objects.get(id=id)
    print(id)
    # new_post = Post()
    if request.method == 'POST':
        newpost = ChatPostForm(request.POST,request.FILES)
        if newpost.is_valid():
            post = newpost.save(commit=False)
            post.poster = request.user
            post.chatroom = chatroom
            print(post.poster)
            post.save()
            return redirect('index')
        return redirect('index')


def chatrooms(request):
    current_user = request.user
    chatrooms = Chatroom.objects.all()

    return render(request,'chatrooms.html',{'chatrooms':chatrooms})


@login_required(login_url='/accounts/login/')
def newchatroom(request):
    current_user = request.user
    if request.method == 'POST':
        NewChatForm = ChatForm(request.POST)
        if NewChatForm.is_valid():
            chatform = NewChatForm.save(commit=False)
            chatform.admin = current_user
            chatform.save()
            print('saved')

            # request.session.modified = True
            # current_user.profile.hood = hoodform.id
        # return redirect('profilehood' + hoodform.name)
        return redirect('index')


    else:
        NewChatForm = ChatForm()
    return render(request, 'forms/newchat.html', {"newChatForm": NewChatForm})



def profilechatrooms(request):
    current_user = request.user
    chatrooms = current_user.profile.chatroom.all()

    return redirect('index')



def joinchat(request,id):
    current_user = request.user
    chat = Chatroom.objects.get(id=id)
    current_user.profile.addchatroom(current_user,chat)
    current_user.profile.save()

    return redirect('index')