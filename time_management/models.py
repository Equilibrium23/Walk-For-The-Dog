from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import datetime
from register_and_login.models import Profile
from dog_editing.models import Dog

class TimePeriod(models.Model):

	TIME_TYPE = [('O', 'occupied'), ('F', 'free')]
	
	person = models.ForeignKey(User, on_delete=models.CASCADE)
	day = models.DateField()
	start_hour = models.TimeField()
	end_hour = models.TimeField()
	time_type = models.CharField(max_length=1, choices=TIME_TYPE, default='F')
	time_name = models.CharField(max_length=100, default='')

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["person","day", "start_hour","end_hour"], name='block duplicate')
		]

class DogTime(models.Model):
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
	dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
	time_period = models.ForeignKey(TimePeriod, on_delete=models.CASCADE)
	match = models.BooleanField(default=False)
	class Meta:
		unique_together = ("dog", "time_period")