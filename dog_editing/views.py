from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddDogForm
from django.contrib.auth.decorators import login_required
from .models import Dog
from django.contrib.auth.models import User
from django.db import connection
import datetime
from django.conf import settings
from ML.utils import make_prediction


@login_required
def add_dog(request):
    if request.method == 'POST':
        form = AddDogForm(request.POST, request.FILES)
        if form.is_valid():
            dog_name = form.cleaned_data['dog_name']
            size = form.cleaned_data['size']
            short_description = form.cleaned_data['short_description']
            image = form.cleaned_data['image']
            cur_user = request.user.profile
            d = Dog(dog_name=dog_name, breed='cokolwiek', size=size, short_description=short_description, image=image, owner_id=cur_user.id)
            d.save()
            d.breed = make_prediction(settings.BASE_DIR + d.image.url, 224)
            d.save()
            messages.success(request, f'Your dog has been added!! Dog\'s breed was recognized by a model. Go check your'
                                      f' dog\'s profile to see if it was right - if not, change it ')
            #close_old_connections()
            return redirect('profile')
    else:
        form = AddDogForm()
    return render(request, 'dog_editing/add_dog.html', {'form':form})


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
    return render(request, 'dog_editing/edit_dog_profile.html', {'form':form})


@login_required
def delete_dog(request):
    request_dog_id = request.GET.get("request_dog_id", "")
    request_dog = Dog.objects.filter(id=request_dog_id).first()
    if request.method == 'POST':
        dog = Dog.objects.filter(id=request_dog_id).delete()
        messages.success(request, f'Your dog has been deleted!!!')
        return redirect('profile')
    return render(request, 'dog_editing/delete_dog.html', {'request_dog':request_dog})
