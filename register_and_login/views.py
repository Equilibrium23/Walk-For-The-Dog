from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.db import connection
import datetime


def login(request):
    return render(request,'register_and_login/login.html') 


def register(request):
    #if request.user.is_authenticated:
    #   return redirect('start_page')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data['name']
            user.profile.account_type = form.cleaned_data['account_type']
            user.profile.location = form.cleaned_data['location']
            user.profile.joining_date = form.cleaned_data['joining_date']
            
            if form.cleaned_data['image']:
                user.profile.image = form.cleaned_data['image']
            user.save()
            #close_old_connections()
            
            return redirect('login')
            
    else:
        form = UserRegisterForm()

    return render(request, 'register_and_login/register.html', {'form': form})









