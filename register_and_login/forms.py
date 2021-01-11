from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
from .models import Profile

class UserRegisterForm(UserCreationForm):

	ACCOUNT_TYPES = [("N", 'needy'), ("H", 'helper')]

	email = forms.EmailField()
	name = forms.CharField(required=True)
	account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)
	location = forms.CharField(required=True)
	image = forms.ImageField(required=False)
	joining_date = forms.DateField(initial=datetime.date.today, widget=forms.HiddenInput())

	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'password1', 'password2', 'account_type', 'location', 'image']

