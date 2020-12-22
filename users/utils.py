from datetime import datetime, timedelta, date
from calendar import HTMLCalendar

from register_and_login.models import TimePeriod
from django.contrib.auth.models import User

def hourly_it(start, finish):
	while finish > start:
		start = start + timedelta(minutes=30)
		yield start

def merge_time_ranges(data):
	result = []
	if(len(data)>0):
		data.sort()
		t_old = data[0]
		for t in data[1:]:
			if t_old[1] == t[0]:
				t_old = ((min(t_old[0], t[0]), max(t_old[1], t[1])))
			else:
				result.append(t_old)
				t_old = t
		else:
			result.append(t_old)
	return result

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, day=None):
		self.year = year
		self.month = month
		self.day = day
		super(Calendar, self).__init__()

	def formatweekheader(self):
		header ='<thead class="font-weight-bold text-uppercase"><tr>'
		weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		for day in weekdays:
			header += f'<th span="col"> {day} </th>'
		header += "</tr></thead>"
		return header

	def formatweekheaderforweek(self, startdate):
		header ='<thead class="font-weight-bold text-uppercase"><tr class="d-flex"><th span="col">time</th>'
		weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		dates = [startdate + timedelta(days=n) for n in range(7)]
		for weekday, d in zip(weekdays, dates):
			header += f'<th span="col"><a href="../calendar/?view=day&date={d.year}-{d.month}-{d.day}"> {weekday} {d.day} </a></th>\n'
		header += "</tr></thead>"
		return header

	def formatmonth(self, ev, withyear=True):
		events = ev.filter(day__year=self.year, day__month=self.month)

		cal = f'<div class="d-flex align-items-center justify-content-center mb-2"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="font-weight-bold text-uppercase">'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}</h2></div>\n'
		cal += f'<table class="table table-hover table-striped table-borderless p-2 mb-0 calendarmonth">'
		cal += f'{self.formatweekheader()}\n'
		cal += f'<tbody>'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += '<tr class="d-flex" style="min-height: 8rem;">'
			for day, weekday in week:
				if day != 0:
					events_per_day = events.filter(day__day=day)
					eventsdata=''
					dates = [(event.start_hour.strftime("%H:%M"), event.end_hour.strftime("%H:%M")) for event in events_per_day]
					e = merge_time_ranges(dates)
					for evnt in e:
						eventsdata += f'<div class="bg-primary"> {evnt[0]}-{evnt[1]} </div>'
					cal += f'<td><a href="../calendar/?view=day&date={self.year}-{self.month}-{day}">{day}</a>{eventsdata}</td>'
				else:
					cal += f'<td></td>'
			cal += '</tr>'
		cal += f'</tbody></table>'
		return cal

	def formatbyweek(self, ev, withyear=True):
		dt = date(self.year, self.month, self.day)
		start = dt - timedelta(days=dt.weekday())
		end = start + timedelta(days=6)
		cal = f'<div class="d-flex align-items-center justify-content-center mb-2"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="font-weight-bold text-uppercase">'
		cal += f'{start.strftime("%d %b")} - {end.strftime("%d %b")} </h2></div>\n'
		cal += f'<table class="table table-hover table-striped table-borderless p-5 small text-center calendarweek">'
		cal += f'{self.formatweekheaderforweek(start)}\n'
		cal += f'<tbody>'

		starthour = datetime(year=2020, month=12, day=11, hour = 5, minute=0)
		finishhour = datetime(year=2020, month=12, day=11, hour = 23, minute=0)
		dates = [start + timedelta(days=n) for n in range(7)]

		for hour in hourly_it(starthour, finishhour):
			cal += f'<tr class="d-flex"><th scope="row">{hour.strftime("%H:%M")}</th>'
			for day in dates:
				events_per_day = ev.filter(day__year=day.year, day__month=day.month, day__day=day.day)
				for event in events_per_day:
					if(event.start_hour.hour==hour.hour and event.start_hour.minute==hour.minute):
						cal += f'<td class="bg-primary">dog time</td>'
				else:
					cal += '<td></td>'
			cal += '</tr>\n'
		cal += f'</tbody></table>'
		return cal

	def formatbyday(self, ev, withyear=True):
		dt = date(self.year, self.month, self.day)
		events = ev.filter(day__year=self.year, day__month=self.month, day__day=self.day)
		cal = f'<div class="d-flex align-items-center justify-content-center mb-2"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="font-weight-bold text-uppercase">'
		cal += f'{dt.strftime("%A, %d %b %Y")} </h2></div>\n'
		cal += f'<table class="table table-hover table-striped table-borderless p-5 small text-center calendarday">'
		cal += f'<thead><tr class="text-uppercase d-flex"><th span="col">time</th><th span="col">Events</th></tr></thead>'
		cal += f'<tbody>'

		starthour = datetime(year=self.year, month=self.month, day=self.day, hour = 5, minute=0)
		finishhour = datetime(year=self.year, month=self.month, day=self.day, hour = 23, minute=0)

		for hour in hourly_it(starthour, finishhour):
			cal += f'<tr class="d-flex"><th scope="row">{hour.strftime("%H:%M")}</th>'
			for event in events:
				if(event.start_hour.hour==hour.hour and event.start_hour.minute==hour.minute):
					cal += f'<td class="bg-primary">dog time</td>'
					break
			else:
				cal += '<td></td>'
			cal += '</tr>\n'
		cal += f'</tbody></table>'
		return cal