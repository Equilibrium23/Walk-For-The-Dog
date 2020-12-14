from datetime import datetime, timedelta, date
from calendar import HTMLCalendar

from register_and_login.models import TimePeriod
from django.contrib.auth.models import User

def hourly_it(start, finish):
	while finish > start:
		start = start + timedelta(minutes=30)
		yield start

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
		header ='<thead class="font-weight-bold text-uppercase"><tr><th span="col">time</th>'
		weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		dates = [startdate + timedelta(days=n) for n in range(7)]
		for weekday, d in zip(weekdays, dates):
			header += f'<th span="col"><a href="../calendar/?view=day&date={d.year}-{d.month}-{d.day}"> {weekday} {d.day} </a></th>\n'
		header += "</tr></thead>"
		return header

	def formatday(self, day, events):
		events_per_day = events.filter(day__day=day)
		d = ''
		for event in events_per_day:
			d += f'<div class="event bg-info"> {event.start_hour.strftime("%H:%M")}-{event.end_hour.strftime("%H:%M")} </div>'

		if day != 0:
			return f'<td><span class="date">{day}</span>{d}</td>'

		return f'<td></td>'

	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr>{week}</tr>'

	def formatmonth(self, ev, withyear=True):
		events = ev.filter(day__year=self.year, day__month=self.month)

		cal = f'<div class="d-flex align-items-center"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="calendartitle font-weight-bold mb-0 text-uppercase">'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}</h2></div>\n'
		cal += f'<table class="table table-hover calendarmonth p-5">'
		cal += f'{self.formatweekheader()}\n'
		cal += f'<tbody class="days">'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += '<tr>'
			for day, weekday in week:
				events_per_day = events.filter(day__day=day)
				if day != 0:
					eventsdata=''
					for event in events_per_day:
						eventsdata += f'<div class="event bg-primary"> {event.start_hour.strftime("%H:%M")}-{event.end_hour.strftime("%H:%M")} </div>'
					cal += f'<td><span class="date"><a href="../calendar/?view=day&date={self.year}-{self.month}-{day}">{day}</a></span>{eventsdata}</td>'
				else:
					cal += f'<td></td>'
			cal += '</tr>'
		cal += f'</tbody></table>'
		return cal

	def formatbyweek(self, ev, withyear=True):
		dt = date(self.year, self.month, self.day)
		start = dt - timedelta(days=dt.weekday())
		end = start + timedelta(days=6)
		cal = f'<div class="d-flex align-items-center"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="calendartitle font-weight-bold mb-0 text-uppercase">'
		cal += f'{start.strftime("%d %b")} - {end.strftime("%d %b")} </h2></div>\n'
		cal += '<div class="table-responsive">\n'
		cal += f'<table class="table table-hover borderless p-5" id="notmonth"><div class="calendarweek">'
		cal += f'{self.formatweekheaderforweek(start)}\n'
		cal += f'<tbody class="days" style="font-size: 1rem;">'

		starthour = datetime(year=2020, month=12, day=11, hour = 5, minute=0)
		finishhour = datetime(year=2020, month=12, day=11, hour = 23, minute=0)
		flag=False
		dates = [start + timedelta(days=n) for n in range(7)]

		for hour in hourly_it(starthour, finishhour):
			cal += f'<tr><th scope="row">{hour.strftime("%H:%M")}</th>'
			for day in dates:
				events_per_day = ev.filter(day__year=day.year, day__month=day.month, day__day=day.day)
				for event in events_per_day:
					if(event.start_hour.hour==hour.hour and event.start_hour.minute==hour.minute):
						cal += f'<td class="event bg-primary" >freetime</td>'
				else:
					cal += '<td></td>'
			cal += '</tr>\n'

		cal += f'</tbody></div></table></div>'

		return cal

	def formatbyday(self, ev, withyear=True):
		dt = date(self.year, self.month, self.day)

		events = ev.filter(day__year=self.year, day__month=self.month, day__day=self.day)

		cal = f'<div class="d-flex align-items-center"><i class="fa fa-calendar fa-3x mr-3"></i>'
		cal += f'<h2 class="calendartitle font-weight-bold mb-0 text-uppercase">'
		cal += f'{dt.strftime("%d %b, %Y %A")} </h2></div>\n'
		cal += '<div class="table-responsive">\n'
		cal += f'<table class="table table-hover borderless p-5" id="notmonth"><div class="calendarday">'

		cal += f'<thead class="font-weight-bold text-uppercase"><tr><th span="col">time</th><th span="col">Events</th></tr></thead>'

		cal += f'<tbody class="days" style="font-size: 1rem;">'

		starthour = datetime(year=self.year, month=self.month, day=self.day, hour = 5, minute=0)
		finishhour = datetime(year=self.year, month=self.month, day=self.day, hour = 23, minute=0)

		for hour in hourly_it(starthour, finishhour):
			cal += f'<tr><th>{hour.strftime("%H:%M")}</th>'
			for event in events:
				if(event.start_hour.hour==hour.hour and event.start_hour.minute==hour.minute):
					cal += f'<td class="event bg-primary" >freetime</td>'
					break
			else:
				cal += '<td></td>'
			cal += '</tr>\n'

		cal += f'</tbody></div></table></div>'

		return cal