from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from register_and_login.models import Profile
import datetime

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