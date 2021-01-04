from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from register_and_login.models import Dog, Profile


@login_required
def profile(request):
    context = { 'dogs' : Dog.objects.all().filter(owner_id=request.user.profile.id) }
    return render(request, 'users/profile.html', context) 

from .matchPeople import matchUsers

def chat(request):
    data = matchUsers(request)
    return render(request, 'users/data.html',{'data':data}) 

from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from register_and_login.models import DogTime, TimePeriod
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

from .googleCalendarUtils import synchronize_with_google_calendar
from django.http import HttpResponseRedirect

def synchronize_calendar(request):
    synchronize_with_google_calendar(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))