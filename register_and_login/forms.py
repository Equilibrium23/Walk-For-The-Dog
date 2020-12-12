from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
from .models import Profile, Dog, TimePeriod

class UserRegisterForm(UserCreationForm):

	ACCOUNT_TYPES = [("1", 'needy'), ("2", 'helper')]

	email = forms.EmailField()
	name = forms.CharField(required=True)
	account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
	location = forms.CharField(required=True)
	image = forms.ImageField(required=False)
	joining_date = forms.DateField(initial=datetime.date.today)

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'password1', 'password2', 'account_type', 'location', 'image']


class AddDogForm(forms.ModelForm):

	DOG_SIZE = [('S', 'small'), ('M', 'medium'), ('B', 'big')]

	class Meta:
		model = Dog
		fields = ['dog_name', 'breed', 'size', 'short_description', 'image']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['name', 'location', 'image']

class NeedyForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['quarantine_time']

class HelperForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['helping_radius', 'max_dog_amount', 'max_dog_size']	

class ChangeAccountForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['account_type']

class AddTimePeriodForm(forms.ModelForm):

	DATE_CHOICE = [ ((datetime.datetime.now() + datetime.timedelta(days=i)).date(), ((datetime.datetime.now() 
					+ datetime.timedelta(days=i)).date()).strftime("%d-%m-%Y")) for i in range(0,8) ]

	HOUR_CHOICE = [ ((datetime.datetime.combine(datetime.date(1,1,1),datetime.time(6,00,00)) + datetime.timedelta(minutes=i)).time(), 
					((datetime.datetime.combine(datetime.date(1,1,1),datetime.time(6,00,00)) + datetime.timedelta(minutes=i)).time()).strftime("%H:%M")) 
					for i in range(0,1080,30) ]

	day = forms.DateField(widget=forms.Select(choices=DATE_CHOICE))
	start_hour = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICE))


	class Meta:
		model = TimePeriod
		fields = ['day', 'start_hour']