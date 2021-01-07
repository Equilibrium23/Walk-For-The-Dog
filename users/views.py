from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register_and_login.models import Profile
from dog_editing.models import Dog


@login_required
def profile(request):
    context = { 'dogs' : Dog.objects.all().filter(owner_id=request.user.profile.id) }
    return render(request, 'users/profile.html', context) 

from .matchPeople import matchUsers

def chat(request):
    # data = matchUsers(request)
    return render(request, 'users/chat.html') 

