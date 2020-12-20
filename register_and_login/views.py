from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, AddDogForm, UserUpdateForm, ProfileUpdateForm
from .forms import NeedyForm, HelperForm, ChangeAccountForm, AddTimePeriodForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Dog, TimePeriod
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

def add_dog(request):

    if request.method == 'POST':
        form = AddDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_name = form.cleaned_data['dog_name']
            breed = form.cleaned_data['breed']
            size = form.cleaned_data['size']
            short_description = form.cleaned_data['short_description']
            image = form.cleaned_data['image']
            cur_user = request.user
            d = Dog(dog_name=dog_name, breed=breed, size=size, short_description=short_description, image=image, owner_id=cur_user.id)
            d.save()
            messages.success(request, f'Your dog has been added!!')
            #close_old_connections()
            return redirect('profile')
    else:
        form = AddDogForm()

    return render(request, 'register_and_login/add_dog.html', {'form':form})



@login_required
def edit_dog_profile(request):

    request_dog_id = request.GET.get("request_dog_id", "")
    dog = Dog.objects.all().filter(id=request_dog_id).first()

    if request.method == 'POST':
        form = AddDogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            
            dog.dog_name = form.cleaned_data['dog_name']
            dog.breed = form.cleaned_data['breed']
            dog.size = form.cleaned_data['size']
            dog.short_description = form.cleaned_data['short_description']
            dog.image = form.cleaned_data['image']
            dog.save()
            messages.success(request, f'Your dog profile has been updated!!')
            #close_old_connections()
            
            return redirect('profile')
    else:
        form = AddDogForm(instance=dog)

    return render(request, 'register_and_login/edit_dog_profile.html', {'form':form})


@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        n_form = NeedyForm(request.POST, instance=request.user.profile)
        h_form = HelperForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            if n_form.is_valid():
                n_form.save()
            elif h_form.is_valid():
                h_form.save()

            u_form.save()
            p_form.save()
                   
            messages.success(request, f'Your account has been updated!')
            #close_old_connections()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        n_form = NeedyForm(instance=request.user.profile)
        h_form = HelperForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'n_form': n_form,
        'h_form': h_form,
    }

    return render(request, 'register_and_login/update.html', context)

@login_required
def change_ac_type(request):
    if request.method == 'POST':
        ca_form = ChangeAccountForm(request.POST, instance=request.user.profile)

        if ca_form.is_valid():
            ca_form.save()
            messages.success(request, f'Your account type has been changed!!!')
            #close_old_connections()
            return redirect('profile')
    else:
        ca_form = ChangeAccountForm(instance=request.user.profile)

    return render(request, 'register_and_login/change_ac_type.html', context)


@login_required
def add_time_period(request):

    if request.method == 'POST':
        form = AddTimePeriodForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            start_hour = form.cleaned_data['start_hour']
            time_length = form.cleaned_data['time_length']

            delta = datetime.timedelta(minutes=30)
            person = request.user
            end_hour = (datetime.datetime.combine(datetime.date(1,1,1),start_hour)+delta).time()
            tp = TimePeriod(person=person, day=day, start_hour=start_hour, end_hour=end_hour)
            tp.save()

            if time_length == 60 or time_length == 90 or time_length == 120:
                d1 = datetime.timedelta(minutes=30)
                sh1 = (datetime.datetime.combine(datetime.date(1,1,1),start_hour)+d1).time()
                eh1 = (datetime.datetime.combine(datetime.date(1,1,1),sh1)+delta).time()
                tp1 = TimePeriod(person=person, day=day, start_hour=sh1, end_hour=eh1)
                tp1.save()

            if time_length == 90 or time_length == 120:
                d1 = datetime.timedelta(minutes=60)
                sh1 = (datetime.datetime.combine(datetime.date(1,1,1),start_hour)+d1).time()
                eh1 = (datetime.datetime.combine(datetime.date(1,1,1),sh1)+delta).time()
                tp1 = TimePeriod(person=person, day=day, start_hour=sh1, end_hour=eh1)
                tp1.save()

            if(time_length == 120):
                d1 = datetime.timedelta(minutes=90)
                sh1 = (datetime.datetime.combine(datetime.date(1,1,1),start_hour)+d1).time()
                eh1 = (datetime.datetime.combine(datetime.date(1,1,1),sh1)+delta).time()
                tp1 = TimePeriod(person=person, day=day, start_hour=sh1, end_hour=eh1)
                tp1.save()
            
            if time_length == 30:
                messages.success(request, f'Your time period has been added!!')
            else:
                messages.success(request, f'Your time periods have been added!!')

            #close_old_connections()
            return redirect('add_time_period')
    else:
        form = AddTimePeriodForm()
    return render(request, 'register_and_login/add_time_period.html', {'form':form})


@login_required
def delete_dog(request):

    request_dog_id = request.GET.get("request_dog_id", "")
    request_dog = Dog.objects.filter(id=request_dog_id).first()

    if request.method == 'POST':
        dog = Dog.objects.filter(id=request_dog_id).delete()
        messages.success(request, f'Your dog has been deleted!!!')
        return redirect('profile')
  
    return render(request, 'register_and_login/delete_dog.html', {'request_dog':request_dog})


@login_required
def delete_profile(request):

    request_user_id = request.GET.get("request_user_id", "")
    request_user = Profile.objects.filter(id=request_user_id).first()
    user_id = request_user.user_id

    if request.method == 'POST':
        user = Profile.objects.filter(id=request_user_id).delete()
        user2 = User.objects.filter(id=user_id).delete()
        messages.success(request, f'Your profile has been deleted!!!')
        return redirect('register')
  
    return render(request, 'register_and_login/delete_profile.html', {'request_user':request_user})

