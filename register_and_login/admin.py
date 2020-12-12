from django.contrib import admin
from .models import Profile, Dog, TimePeriod

admin.site.register(Profile)
admin.site.register(Dog)
admin.site.register(TimePeriod)
