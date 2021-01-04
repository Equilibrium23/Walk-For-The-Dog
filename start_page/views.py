from django.shortcuts import render
from django.db import connection
from register_and_login.models import Dog, Profile
from users.matchPeople import matchUsers
from .utils import mergeTimes

def start_page(request):
	#close_old_connections()
	if request.user.is_authenticated:
		matches = mergeTimes(matchUsers(request))
		context = { 'matches' : matches }
		return render(request,'start_page/start_page.html', context)
	else:
		return render(request,'start_page/start_page.html')

