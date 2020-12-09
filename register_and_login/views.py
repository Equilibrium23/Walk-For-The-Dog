from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, AddDogForm, UserUpdateForm, ProfileUpdateForm, NeedyForm, HelperForm, ChangeAccountForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Dog
from django.contrib.auth.models import User


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
        n_form = NeedyForm(request.POST, instance=request.user.profile)
        h_form = HelperForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid() and n_form.is_valid() and h_form.is_valid():
            u_form.save()
            p_form.save()
            n_form.save()
            h_form.save()
            messages.success(request, f'Your account has been updated!')
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
            messages.success(request, f'Your account type has been changed!')
            return redirect('profile')
    else:
        ca_form = ChangeAccountForm(instance=request.user.profile)

    return render(request, 'register_and_login/change_ac_type.html', {'ca_form':ca_form})