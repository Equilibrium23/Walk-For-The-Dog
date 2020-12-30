from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register_and_login.models import Dog, Profile


@login_required
def profile(request):
    context = { 'dogs' : Dog.objects.all().filter(owner_id=request.user.profile.id) }

    return render(request, 'users/profile.html', context) 

GOOGLE_MAP_KEY = 'AIzaSyBBcPbX-93uzhQq9qQosN7TzVYGtr3cFpg'
import urllib.request
import json

def check_location(location_A,location_B,helping_radius):
    url = '''https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={}&destinations={}&key={}'''.format(location_A,location_B,GOOGLE_MAP_KEY)
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    status = result['rows'][0]['elements'][0]['status']
    if status == 'OK':
        distance = [result['rows'][0]['elements'][0]['distance']['text'],{'m':result['rows'][0]['elements'][0]['distance']['value']}]
        # with open("data.txt",'w') as file: # Use file to refer to the file object
        #     file.write(str(distance[1]['m']))
        # expected_time = [result['rows'][0]['elements'][0]['duration']['text'],{'s':result['rows'][0]['elements'][0]['duration']['value']}]
        return True if float(distance[1]['m']) <= float(helping_radius*1000) else False 


def chat(request):
    data = []
    temp_user = Profile.objects.all().filter(user = request.user)
    helpers = Profile.objects.all().filter(account_type='H')
    list_of_helpers = [ helpers[i].id for i in range(helpers.count()) if check_location( temp_user[0].location, helpers[i].location, helpers[i].helping_radius) ]
    return render(request, 'users/data.html',{'data':list_of_helpers}) 

























from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from register_and_login.models import TimePeriod
from .utils import Calendar

class CalendarView(generic.ListView):
    model = TimePeriod
    template_name = 'users/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view = self.request.GET.get('view', None)
        date = self.request.GET.get('date', None)
        user = self.request.user
        events = TimePeriod.objects.filter(person=user)
        if date:
            d = datetime.strptime(date, '%Y-%m-%d')
        else:
            d = datetime.now()
        cal = Calendar(d.year, d.month, d.day)
        if view=='day':
            html_cal = cal.formatbyday(events, withyear=True)
            context['prev_view'] = (d - timedelta(days=1)).strftime("%Y-%m-%d")
            context['next_view'] = (d + timedelta(days=1)).strftime("%Y-%m-%d")
        elif view=='week':
            html_cal = cal.formatbyweek(events, withyear=True)
            context['prev_view'] = (d - timedelta(days=7)).strftime("%Y-%m-%d")
            context['next_view'] = (d + timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            html_cal = cal.formatmonth(events, withyear=True)
            context['prev_view'] = (d.replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
            context['next_view'] = (d.replace(day=calendar.monthrange(d.year, d.month)[1]) + timedelta(days=1)).strftime("%Y-%m-%d")

        context['calendar'] = mark_safe(html_cal)
        return context

from .utils import synchronize_with_google_calendar

def synchronize_calendar(request):
    synchronize_with_google_calendar(request)
    ####
    return render(request, 'users/calendar.html') 