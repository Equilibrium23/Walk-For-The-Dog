from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import datetime
from .models import Dog

class AddDogForm(forms.ModelForm):

	DOG_SIZE = [('S', 'small'), ('M', 'medium'), ('B', 'big')]

	class Meta:
		model = Dog
		fields = ['dog_name', 'breed', 'size', 'short_description', 'image']