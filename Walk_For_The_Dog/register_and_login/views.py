from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, AddDogForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Dog
from django.contrib.auth.models import User
#from datetime import datetime


def login(request):
    return render(request,'register_and_login/login.html') 


def register(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data['name']
            user.profile.account_type = form.cleaned_data['account_type']
            user.profile.location = form.cleaned_data['location']
            user.profile.joining_date = form.cleaned_data['joining_date']
            #user.profile.joining_date = timezone.now();
            user.save()
            
            return redirect('login')
            
    else:
        form = UserRegisterForm()

    return render(request, 'register_and_login/register.html', {'form': form})

def add_dog(request):

    if request.method == 'POST':
        form = AddDogForm(request.POST)
        if form.is_valid():
            dog_name = form.cleaned_data['dog_name']
            breed = form.cleaned_data['breed']
            size = form.cleaned_data['size']
            short_description = form.cleaned_data['short_description']
            cur_user = request.user
            d = Dog(dog_name=dog_name, breed=breed, size=size, short_description=short_description, owner_id=cur_user.id)
            d.save()
            messages.success(request, f'Your dog has been added!!')
            return redirect('profile')
    else:
        form = AddDogForm()

    return render(request, 'register_and_login/add_dog.html', {'form':form})




@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'register_and_login/update.html', context)