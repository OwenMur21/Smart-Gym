from django.shortcuts import render
import json
import urllib
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import SignupForm
from .decorators import check_recaptcha


# Create your views here.
def trainer(request):
    profiles = Profile.objects.all()
    
    return render(request,'profile/profile.html',{ "profiles":profiles })
def profile(request, user_id):
    """
    Function that enables one to see their profile
    """
    title = "Profile"
    profiles = User.objects.get(id=user_id)
    user = User.objects.get(id=user_id)
    return render(request, 'profile/profile.html',{'title':title, "profiles":profiles})

  
def new_profile(request):
    current_user = request.user
    profile=Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
        return redirect('/')

    else:
        form = ProfileForm()
    return render(request, "profile/edit_profile.html", {"form":form}) 

def homepage(request):
    return render(request, 'home.html')

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