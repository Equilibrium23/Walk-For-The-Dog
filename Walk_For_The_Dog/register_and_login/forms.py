from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
from .models import Profile

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

	dog_name = forms.CharField(max_length=50)
	breed = forms.CharField(max_length=100)
	size = forms.CharField(max_length=100)
	short_description = forms.CharField(max_length=300)
	image = forms.ImageField(required=False)

	class Meta:
		model = User
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
