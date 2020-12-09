from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime

class Profile(models.Model):

	ACCOUNT_TYPES = [("1", 'needy'), ("2", 'helper')]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, blank=False)
	account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPES, default='1')
	location = models.CharField(max_length=30, blank=False, default='')
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')#, blank=True)
	joining_date = models.DateField(auto_now_add=True, blank=True)
	#joining_date = models.DateField(blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)

		img=Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class Dog(models.Model):

	dog_name = models.CharField(max_length=50)
	breed = models.CharField(max_length=100)
	size = models.CharField(max_length=100)
	short_description = models.CharField(max_length=300)
	image = models.ImageField(default='profile_pics/dog_default.jpg', upload_to='profile_pics')#, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE) 
	
	def __str__(self):
		return self.dog_name

	def save(self, *args, **kwargs):
		super(Dog, self).save(*args, **kwargs)

		img=Image.open(self.image.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)