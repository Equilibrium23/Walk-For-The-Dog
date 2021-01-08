from django.shortcuts import render
from django.db import connection
from users.matchPeople import matchUsers
from .utils import mergeTimes

def start_page(request):
	if request.user.is_authenticated:
		matches = mergeTimes(matchUsers(request))
		context = { 'matches' : matches }
		return render(request,'start_page/start_page.html', context)
	else:
		return render(request,'start_page/start_page.html')

