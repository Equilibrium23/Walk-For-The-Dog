from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile(request):
    return render(request,'users/profile.html') 

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
        d = get_date(date)
        cal = Calendar(d.year, d.month, d.day)
        if view=='day':
            html_cal = cal.formatbyday(events, withyear=True)
            context['prev_view'] = prev_day(d)
            context['next_view'] = next_day(d)
        elif view=='week':
            html_cal = cal.formatbyweek(events, withyear=True)
            context['prev_view'] = prev_week(d)
            context['next_view'] = next_week(d)
        else:
            html_cal = cal.formatmonth(events, withyear=True)
            context['prev_view'] = prev_month(d)
            context['next_view'] = next_month(d)

        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month, day = (int(x) for x in req_day.split('-'))
        return date(year, month, day)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month) + '-1'
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month) + '-1'
    return month

def prev_day(d):
    prev_date = d - timedelta(days=1)
    day = str(prev_date.year) + '-' + str(prev_date.month) + '-' + str(prev_date.day)
    return day

def next_day(d):
    next_date = d + timedelta(days=1)
    day = str(next_date.year) + '-' + str(next_date.month) + '-' + str(next_date.day)
    return day

def prev_week(d):
    prev_date = d - timedelta(days=7)
    day = str(prev_date.year) + '-' + str(prev_date.month) + '-' + str(prev_date.day)
    return day

def next_week(d):
    next_date = d + timedelta(days=7)
    day = str(next_date.year) + '-' + str(next_date.month) + '-' + str(next_date.day)
    return day

def event(request):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

def event(request):
    context = {
        'event':ev
    }
    return render(request, 'users/calendar.html', context)
