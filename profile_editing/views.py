from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .forms import NeedyForm, HelperForm, ChangeAccountForm
from django.contrib.auth.decorators import login_required
from register_and_login.models import Profile
from django.contrib.auth.models import User
from django.db import connection
import datetime


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

    return render(request, 'profile_editing/update.html', context)

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

    context = {
        'ca_form':ca_form
    }

    return render(request, 'profile_editing/change_ac_type.html', context)

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
  
    return render(request, 'profile_editing/delete_profile.html', {'request_user':request_user})

