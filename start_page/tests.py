from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestStartPageViews(TestCase):
    def test_start_page_get_site_user_is_not_authenticated(self):
        url = reverse('start_page')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'start_page/start_page.html')

# class TestStartPageAcceptDecline(TestCase):
#     def setUp(self):
#         self.test_username = 'test'
#         self.test_password = 'test'
#         test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
#         test_user.save()
#         self.client.login(username='test', password='test')

#     def test_decline(self):
#         url = reverse('decline')
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#         self.assertRedirects('start_page')

    # def test_accept(self):
    #     url = reverse('accept')
    #     response = self.client.get(url)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertRedirects('start_page')