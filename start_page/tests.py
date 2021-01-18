from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from register_and_login.models import Profile
from users.models import Match
from time_management.models import TimePeriod

class TestStartPageViews(TestCase):
    def test_start_page_get_site_user_is_not_authenticated(self):
        url = reverse('start_page')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'start_page/start_page.html')
    
    def test_start_page_get_site_needy_is_authenticated(self):
        self.test_username = 'test'
        self.test_password = 'test'
        test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        test_user.save()
        self.client.login(username='test', password='test')

        url = reverse('start_page')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'start_page/start_page.html')
    
    def test_start_page_get_site_helper_is_authenticated(self):
        self.test_username = 'test'
        self.test_password = 'test'
        test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        test_user.save()
        self.client.login(username='test', password='test')
        Profile.objects.get(user=test_user).account_type = 'H'

        url = reverse('start_page')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'start_page/start_page.html')

class TestStartPageAcceptDecline(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')

        self.test_username2 = 'test2'
        self.test_password2 = 'test2'
        self.test_user2 = User.objects.create_user(username=self.test_username2, password=self.test_password2)
        self.test_user2.save()
        Profile.objects.get(user = self.test_user2).account_type = 'H'

        self.time = TimePeriod.objects.create(person = self.test_user,
                                    day = '2021-01-11',
                                    start_hour = '08:00:00',
                                    end_hour = '08:30:00')

        self.time2 = TimePeriod.objects.create(person = self.test_user2,
                                    day = '2021-01-11',
                                    start_hour = '08:00:00',
                                    end_hour = '08:30:00')

        Match.objects.create(dog_id = 1,
                            owner_time_period_id = self.time.id,
                            owner_id = self.test_user.id,
                            helper_time_period_id = self.time2.id,
                            helper_id = self.test_user2.id)

    def test_accept(self):
        url = reverse('accept')
        response = self.client.get(url+"?dogid=1&helperid={}&timeperiodid={}".format(self.test_user2.id,self.time.id))
        self.assertEquals(response.status_code, 302)
        response_url = reverse('start_page')
        self.assertRedirects(response,response_url)
    
    def test_decline(self):
        url = reverse('decline')
        response = self.client.get(url+"?dogid=1&helperid={}&timeperiodid={}".format(self.test_user2.id,self.time.id))
        self.assertEquals(response.status_code, 302)
        response_url = reverse('start_page')
        self.assertRedirects(response,response_url)