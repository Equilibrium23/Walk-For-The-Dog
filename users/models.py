from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    dog_id = models.IntegerField(default = -1) 
    owner_time_period_id = models.IntegerField(default = -1)
    owner_id = models.IntegerField(default = -1)
    helper_time_period_id = models.IntegerField(default = -1)
    helper_id = models.IntegerField(default = -1)
    is_accepted = models.BooleanField(default = False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["dog_id","owner_time_period_id", "owner_id","helper_time_period_id","helper_id","is_accepted"], name='match duplicate')
		]