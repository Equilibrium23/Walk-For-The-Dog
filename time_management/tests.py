from django.test import TestCase
from datetime import datetime
from .googleCalendarUtils import end_of_month, save_data
import random
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.urls import reverse
from register_and_login.models import Profile
from dog_editing.models import Dog
from django.db import IntegrityError
from django.contrib import messages


class TestGoogleCalendarsUtils(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')

    def test_end_of_january_2021(self):
        input_year = 2021 
        input_month = 1
        input_day = 5
        input_hour = random.randint(0,23)
        input_minute = random.randint(0,59)
        input_second = random.randint(0,59)
        test_date = datetime(input_year,input_month,input_day,input_hour,input_minute,input_second).isoformat()+'Z'
        end_of_january_2021_day = 31
        expected_day = datetime(input_year,input_month,end_of_january_2021_day,23,59,59).isoformat()+'Z'
        result = end_of_month(test_date)
        self.assertEquals(result,expected_day)
        
    def test_saving_good_data_from_calendar_api(self):
        request = HttpRequest()
        request.method = 'GET'
        request.user = self.test_user
        start_event = '2021-01-29T11:00:00+01:00'
        end_event = '2021-01-29T12:00:00+01:00'
        event_name = 'test'
        result = save_data(request,start_event,end_event,event_name)
        self.assertEquals(result,True)

    def test_saving_bad_data_from_calendar_api(self):
        request = HttpRequest()
        request.method = 'GET'
        request.user = self.test_user
        start_event = '2021-01-29 11:00:00+01:00'
        end_event = '2021-01-29 12:00:00+01:00'
        event_name = 'test'
        result = save_data(request,start_event,end_event,event_name)
        self.assertEquals(result,False)
    
    def test_saving_duplicated_data_from_calendar_api(self):
        request = HttpRequest()
        request.method = 'GET'
        request.user = self.test_user
        start_event = '2021-01-29T11:00:00+01:00'
        end_event = '2021-01-29T12:00:00+01:00'
        event_name = 'test'
        result = True
        for _ in range(2):
            if save_data(request,start_event,end_event,event_name) == False:
                result = False
        self.assertEquals(result,False)
        
    def test_get_synchronize_with_google_calendar(self):
        url = reverse('synchronize_calendar')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)

class TestTimeManagementViews(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')
        user_profile = Profile.objects.get(user=self.test_user)
        user_profile.account_type = 'H'
        user_profile.save()

    def test_get_add_time_period(self):
        url = reverse('add_time_period')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'time_management/add_time_period.html')

    def test_post_good_data_add_time_period_helper(self):
        url = reverse('add_time_period')
        add_time_period_data = {
            "csrfmiddlewaretoken": "CGzzJeUQIAYJ7DvHnDMv0xLMmzKmjd7J61AGGZpGYrmDYMMGcMmsP6c9uviAnCMz",
            "day": "2021-01-17",
            "start_hour": "06:00:00",
            "time_length": "30",
        }
        response = self.client.post(url, add_time_period_data)
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('add_time_period')
        self.assertRedirects(response, redirect_url)

    def test_post_good_data_add_time_period_needy(self):
        user_profile = Profile.objects.get(user=self.test_user)
        user_profile.account_type = 'N'
        user_profile.save()
        user_dog = Dog.objects.create(dog_name='test', breed='kundel',short_description = 'piekny pies',owner = user_profile )
        url = reverse('add_time_period')
        add_time_period_data = {
            "csrfmiddlewaretoken": "CGzzJeUQIAYJ7DvHnDMv0xLMmzKmjd7J61AGGZpGYrmDYMMGcMmsP6c9uviAnCMz",
            "day": "2021-01-17",
            "start_hour": "06:00:00",
            "time_length": "30",
            "dogs_choice": "{}".format(user_dog.id)
        }
        response = self.client.post(url, add_time_period_data)
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('add_time_period')
        self.assertRedirects(response, redirect_url)

    def test_post_bad_data_add_time_period(self):
        url = reverse('add_time_period')
        add_time_period_data = {
            "csrfmiddlewaretoken": "CGzzJeUQIAYJ7DvHnDMv0xLMmzKmjd7J61AGGZpGYrmDYMMGcMmsP6c9uviAnCMz",
            "day": "2021-01-17",
            "test": "06:00:00",
            "time_length": "30",
        }
        response = self.client.post(url, add_time_period_data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'time_management/add_time_period.html')

    def get_load_calendar_data(self):
        url = reverse('oauth2callback')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response,'calendar')
    
    
