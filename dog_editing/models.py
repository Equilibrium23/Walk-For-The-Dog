from django.db import models
from django.contrib.auth.models import User
from register_and_login.models import Profile
from PIL import Image
from datetime import datetime

class Dog(models.Model):

	DOG_SIZE = [('S', 'small'), ('M', 'medium'), ('B', 'big')]

	dog_name = models.CharField(max_length=50)
	breed = models.CharField(max_length=100)
	size = models.CharField(max_length=1, choices=DOG_SIZE, default='S')
	short_description = models.CharField(max_length=300)
	image = models.ImageField(default='profile_pics/dog_default.jpg', upload_to='profile_pics/')
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE) 
	
	def __str__(self):
		return self.dog_name


