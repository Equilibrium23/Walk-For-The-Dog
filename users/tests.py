from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
#######################################################
from .googleMapsUtils import check_location
#######################################################
from dog_editing.models import Dog
from time_management.models import DogTime, TimePeriod
from register_and_login.models import Profile
from users.matchPeople import check_dog_size
import datetime

class TestUsersViews(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        test_user.save()
        self.client.login(username='test', password='test')

    def test_profile_get_site(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'users/profile.html')

    def test_chat_get_site(self):
        url = reverse('chat')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'users/chat.html')

class TestGoogleMatrixApi(SimpleTestCase):
    ################## check_location(location_A,location_B,helping_radius) ####################
    def test_good_distance(self):
        location_A = 'Krakow'
        location_B = 'Krakow'
        distance = 100
        result = check_location(location_A,location_B,distance)
        self.assertEquals(result,True)

    def test_bad_distance(self):
        location_A = 'Krakow'
        location_B = 'Warszawa'
        distance = 10
        result = check_location(location_A,location_B,distance)
        self.assertEquals(result,False)

    def test_negative_distance(self):
        location_A = 'Krakow'
        location_B = 'Warszawa'
        distance = -1
        result = check_location(location_A,location_B,distance)
        self.assertEquals(result,False)

class TestMatchPeople(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')
        self.dog_owner = Profile.objects.get(user=self.test_user)
        self.test_dog = Dog.objects.create(dog_name='test', breed='kundel', short_description='piekny pies',
                                           owner=self.dog_owner)
        self.test_dog.save()
        self.time_period = TimePeriod.objects.create(person=self.test_user, day=datetime.date(2021, 1, 11),start_hour = datetime.time(8, 0), end_hour=datetime.time(8, 30))
        self.time_period.save()
        self.dog_time = DogTime.objects.create(owner=self.dog_owner,dog=self.test_dog, time_period=self.time_period)
        self.dog_time.save()

    def test_check_dog_size(self):
        temp_user_dogs_need_walk = DogTime.objects.all().filter(owner_id = self.dog_owner.id).filter(match=False)
        print(temp_user_dogs_need_walk)
        result = check_dog_size(temp_user_dogs_need_walk,'S')
        self.assertEquals(result[1], True)





