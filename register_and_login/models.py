from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime

class Profile(models.Model):

	ACCOUNT_TYPES = [("N", 'needy'), ("H", 'helper')]
	DOG_SIZE = [('S', 'small'), ('M', 'medium'), ('B', 'big')]
	DOG_AMOUNT = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=20, blank=False)
	account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPES, default='N')
	location = models.CharField(max_length=30, blank=False, default='')
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics/')
	joining_date = models.DateField(auto_now_add=True, blank=True)
	helping_radius = models.IntegerField(choices=[(i,i) for i in range(1,11)], default=0)
	max_dog_amount = models.IntegerField(choices=DOG_AMOUNT, default=0)
	max_dog_size = models.CharField(max_length=5, choices=DOG_SIZE, default='N')
	quarantine_time = models.IntegerField(choices=[(i,i) for i in range(0,15)], default=0)

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

	DOG_SIZE = [('S', 'small'), ('M', 'medium'), ('B', 'big')]

	dog_name = models.CharField(max_length=50)
	breed = models.CharField(max_length=100)
	size = models.CharField(max_length=1, choices=DOG_SIZE, default='S')
	short_description = models.CharField(max_length=300)
	image = models.ImageField(default='profile_pics/dog_default.jpg', upload_to='profile_pics/')
	owner = models.ForeignKey(User, on_delete=models.CASCADE) 
	
	def __str__(self):
		return self.dog_name


class TimePeriod(models.Model):

	
	person = models.ForeignKey(User, on_delete=models.CASCADE)
	day = models.DateField()
	start_hour = models.TimeField()
	end_hour = models.TimeField()

	class Meta:
		unique_together = (("day", "start_hour"), ("day", "end_hour"), ("start_hour","end_hour"))
	def __str__(self):
		return f'{self.day} -> {self.start_hour} - {self.end_hour} '
