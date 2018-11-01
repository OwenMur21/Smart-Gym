from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import *
# from .forms import *



# Create your views here.
@login_required(login_url='/accounts/login/')
def gymprofile(request):
    current_user = request.user
    current_manager = request.user.gymmanager

    gym = Gym.objects.get(manager = current_user)
    return render(request, 'templates/gym/gymprofile.html, {'gym':gym})

