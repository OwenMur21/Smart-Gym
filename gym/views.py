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
from .forms import SignupForm,GymForm
from .models import *
from .decorators import check_recaptcha



# Create your views here.
@login_required(login_url='/accounts/login/')
def gymprofile(request):
    current_user = request.user
    current_manager = request.user.gymmanager

    gym = Gym.objects.get(manager = current_user)
    return render(request, 'templates/gym/gymprofile.html',{'gym':gym})


def homepage(request):
  gyms = Gym.objects.all()
  return render(request, 'gym/gym.html',locals())

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
def add_gym(request):
	'''
	View function that enables gym admins add their gyms
	'''
	if request.method == 'POST':
		form = GymForm(request.POST,request.FILES)
		if form.is_valid():
			gym = form.save(commit = False)
			gym.user = request.user
			gym.save()
			
			return redirect('home')

	else:
		form = GymForm()
		return render(request,'gym/add_gym.html',locals())

@login_required(login_url='/accounts/login/')
def edit_gym(request,gym_id):
	'''
	View function that enable gym admins edit gym details
	'''
	gyms = Gym.objects.get(pk = gym_id)
	if request.method == 'POST':
		form = GymForm(request.POST,instance = gyms)
		if form.is_valid():
			form.save()
			messages.success(request, 'Gym has been edited successfully')
			
			return redirect('home')
	else:
		form = GymForm(instance = gyms)
		return render(request,'gym/edit_gym.html',locals())
