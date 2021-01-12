from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from users.matchPeople import matchUsers
from users.matchPeople import getMatches
from users.models import Match
from register_and_login.models import Profile
from .utils import mergeTimes
from .utils import get_helper_matches

def start_page(request):
	if request.user.is_authenticated:
		user_profile = Profile.objects.all().get(user = request.user)
		if user_profile.account_type == 'N':
			matchUsers(request)
			match_data = getMatches(request)
			matches = mergeTimes(match_data)
			context = { 'matches' : matches }
			return render(request,'start_page/start_page.html', context)
		elif user_profile.account_type == 'H':
			match_data = get_helper_matches(request)
			matches = mergeTimes(match_data)
			#############################################
			context = { 'matches' : matches }
			return render(request,'start_page/start_page.html', context)
			#############################################
		

	else:
		return render(request,'start_page/start_page.html')


def accept(request):
	
	
	
	#matchUsers_obj = Match.objects.get(id=match_id)
	#matchUsers_obj.value = 'true'
	#matchUsers_obj.save()

	messages.success(request, f'Accept-success')
	return redirect('start_page')

	
def decline(request):
	#matchUsers.objects.get(id=match_id).delete()

	messages.success(request, f'Decline-success')
	return redirect('start_page')

	#time_id = request.GET.get("","") #owner time period id

			