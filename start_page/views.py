from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from users.matchPeople import matchUsers
from users.matchPeople import getMatches
from users.models import Match
from register_and_login.models import Profile
from time_management.models import TimePeriod
from .utils import get_helper_matches

def start_page(request):
	if request.user.is_authenticated:
		user_profile = Profile.objects.all().get(user = request.user)
		if user_profile.account_type == 'N':
			matchUsers(request)
			match_data = getMatches(request)
			context = { 'matches' : match_data }
			return render(request,'start_page/start_page.html', context)
		elif user_profile.account_type == 'H':
			match_data = get_helper_matches(request)
			#############################################
			context = { 'matches' : match_data }
			return render(request,'start_page/start_page.html', context)
			#############################################
		

	else:
		return render(request,'start_page/start_page.html')


def accept(request):
	
	ownertimeperiodid = request.GET.get("timeperiodid", None)
	helperid = request.GET.get("helperid", None)
	dogid = request.GET.get("dogid", None)

	match = Match.objects.filter(dog_id=dogid).filter(helper_id=helperid).filter(owner_time_period_id=ownertimeperiodid).first()
	matchid = match.id
	
	owntimeperiod = TimePeriod.objects.get(id=ownertimeperiodid)
	owntimeperiod.time_type = 'O'
	owntimeperiod.time_name = 'Dog walking'
	owntimeperiod.save()

	helptimeperiod = TimePeriod.objects.filter(person_id=helperid).filter(day=owntimeperiod.day).filter(start_hour=owntimeperiod.start_hour).first()
	helptimeperiod.time_type = 'O'
	helptimeperiod.time_name = 'Dog walking'
	helptimeperiod.save()

	matchUsers_obj = Match.objects.get(id=matchid)
	matchUsers_obj.is_match_accepted = True
	matchUsers_obj.save()
	
	messages.success(request, f'The match is accepted!')
	return redirect('start_page')

	
def decline(request):

	ownertimeperiodid = request.GET.get("timeperiodid", None)
	helperid = request.GET.get("helperid", None)
	dogid = request.GET.get("dogid", None)

	match = Match.objects.filter(dog_id=dogid).filter(helper_id=helperid).filter(owner_time_period_id=ownertimeperiodid).first()
	matchid = match.id
	Match.objects.get(id=matchid).delete()

	messages.success(request, f'The match is declined!')
	return redirect('start_page')


			