from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestStartPageViews(TestCase):
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