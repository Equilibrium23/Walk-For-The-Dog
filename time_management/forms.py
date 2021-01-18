from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
from dog_editing.models import Dog
from .models import TimePeriod

class AddTimePeriodForm(forms.ModelForm):

	DATE_CHOICE = [ ((datetime.datetime.now() + datetime.timedelta(days=i)).date(), ((datetime.datetime.now() 
					+ datetime.timedelta(days=i)).date()).strftime("%d-%m-%Y")) for i in range(0,8) ]

	HOUR_CHOICE = [ ((datetime.datetime.combine(datetime.date(1,1,1),datetime.time(6,00,00)) + datetime.timedelta(minutes=i)).time(), 
					((datetime.datetime.combine(datetime.date(1,1,1),datetime.time(6,00,00)) + datetime.timedelta(minutes=i)).time()).strftime("%H:%M")) 
					for i in range(0,1080,30) ]

	TIME_DELTA_CHOICE = [ (30, "30 min"), (60, "60 min"), (90, "90 min"), (120, "120 min")]

	day = forms.DateField(widget=forms.Select(choices=DATE_CHOICE))
	start_hour = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICE))
	time_length = forms.IntegerField(widget=forms.Select(choices=TIME_DELTA_CHOICE))

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(AddTimePeriodForm, self).__init__(*args, **kwargs)
		
		'''DOG_CHOICE = []
		dogs = Dog.objects.all().filter(owner_id=user.profile.id)
		for d in dogs:
			DOG_CHOICE.append((d.id, d.dog_name))
		self.fields['dogs_choice'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DOG_CHOICE)
'''
	class Meta:
		model = TimePeriod
		fields = ['day', 'start_hour']

class AddTimePeriodFormN(AddTimePeriodForm):

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(AddTimePeriodForm, self).__init__(*args, **kwargs)

		DOG_CHOICE = []
		dogs = Dog.objects.all().filter(owner_id=user.profile.id)
		for d in dogs:
			DOG_CHOICE.append((d.id, d.dog_name))
		self.fields['dogs_choice'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DOG_CHOICE)
