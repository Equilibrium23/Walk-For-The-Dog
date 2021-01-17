from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddTimePeriodForm, AddTimePeriodFormN
from django.contrib.auth.decorators import login_required
from .models import TimePeriod, DogTime
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime, timedelta, date
from django.db import IntegrityError


@login_required
def add_time_period(request):
    if request.method == 'POST':
        if request.user.profile.account_type=='N':
            form = AddTimePeriodFormN(request.POST, user=request.user)
        else:
            form = AddTimePeriodForm(request.POST, user=request.user)
        if form.is_valid():
            day = form.cleaned_data['day']
            start_hour = form.cleaned_data['start_hour']
            time_length = form.cleaned_data['time_length']


            delta = timedelta(minutes=30)
            person = request.user

            time_list_id=[]
            for i in range(0, time_length, 30):
                d1 = timedelta(minutes=i)
                sh1 = (datetime.combine(date(1,1,1),start_hour)+d1).time()
                eh1 = (datetime.combine(date(1,1,1),sh1)+delta).time()
                tp1 = TimePeriod(person=person, day=day, start_hour=sh1, end_hour=eh1, time_type='F', time_name='')
                try:
                    tp1.save()
                    time_list_id.append(tp1.id)
                except IntegrityError as err:
                    messages.error(request, 'You are already occupied this time!')
                    return redirect('add_time_period')
                
            if request.user.profile.account_type=='N':
                dogs = form.cleaned_data['dogs_choice']
                for dog in dogs:
                    d = int(dog)
                    #d = Dog.objects.all().filter(owner_id=request.user.profile.id).filter(dog_id=dog.id).first()
                    for tp in time_list_id:
                        DogTime(owner_id=request.user.profile.id, dog_id=d, time_period_id=tp, match=False).save()
                

            if time_length == 30:
                messages.success(request, f'Your time period has been added!!')
            else:
                messages.success(request, f'Your time periods have been added!!')

            return redirect('add_time_period')
    else:
        if request.user.profile.account_type=='N':
            form = AddTimePeriodFormN(user=request.user)
        else:
            form = AddTimePeriodForm(user=request.user)
    return render(request, 'time_management/add_time_period.html', {'form':form})

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .utils import Calendar

class CalendarView(generic.ListView):
    model = TimePeriod
    template_name = 'time_management/calendar.html'

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
from .googleCalendarUtils import load_data

def synchronize_calendar(request):
    url = synchronize_with_google_calendar(request)
    return redirect(url)

def load_calendar_data(request):
    load_data(request)
    return redirect('calendar')