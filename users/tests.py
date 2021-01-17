from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
#######################################################
from .googleMapsUtils import check_location
#######################################################

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
    ################### check_location(location_A,location_B,helping_radius) #################### 
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

