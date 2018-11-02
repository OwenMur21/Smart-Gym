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
from .forms import *
from .models import *
from .decorators import check_recaptcha



# Create your views here.
def client_home(request):

    return render(request, 'client/client.html')

def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
  
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                messages.success(request, 'Account verified successfully!')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'registration/registration_form.html', {'form': form})

@check_recaptcha
def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'registration/registration_form.html', {'form': form})




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
        return render(request, 'chatroom/chatroom.html', {'chatroom': r,'form':form})


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

    return render(request,'chatroom/chatrooms.html',{'chatrooms':chatrooms})


def exitchatroom(request,id):
    current_user = request.user
    # hood_name = current_user.profile.hood
    # hood = Hood.objects.get(id=id)
    current_user.profile.chatroom = None
    current_user.profile.save()

    return redirect('index')


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
    return render(request, 'client/newchat.html', {"newChatForm": NewChatForm})



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


@login_required(login_url='/accounts/login/')
def people(request):
    people = User.objects.all()

    return render(request,'client/people.html',{'people':people})



@login_required(login_url='/accounts/login/')
def stalk(request,profile_id):
    stalked_user = User.objects.get(pk=profile_id)
    stalked_profile = Trainee.objects.get(user_id=profile_id)

    # profile = Profile.objects.get(user=stalked_user)
    # print(profile)
    posts = Post.objects.filter(poster=stalked_user)
    chatrooms = stalked_user.profile.chatroom.all()
    print(chatrooms)
    # profile = Profile.objects.filter(user=request.user.id)

    return render(request, 'profile/profile.html', {'profile': stalked_profile, 'posts': posts, 'chatrooms': chatrooms})

