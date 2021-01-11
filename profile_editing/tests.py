from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class TestProfileEditingViews(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')

    ######################### update(request) ########################################
    def test_update_get_site(self):
        url = reverse('update')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'profile_editing/update.html')

    def test_update_bad_data_posted(self):
        url = reverse('update')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'profile_editing/update.html')
    
    def test_update_bad_data_posted(self):
        url = reverse('update')
        data ={
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'email':'test@test.pl',
            'name':'test',
            'location':'Warszawa',
            'image':'',
            'quarantine_time':'1',
        }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('profile')
        self.assertRedirects(response,redirect_url)
    
    ######################### change_ac_type(request) ########################################
    def test_change_ac_type_get_site(self):
        url = reverse('change_ac_type')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'profile_editing/change_ac_type.html')

    def test_change_ac_type_bad_data_posted(self):
        url = reverse('change_ac_type')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'profile_editing/change_ac_type.html')
    
    def test_change_ac_type_good_data_posted(self):
        url = reverse('change_ac_type')
        data ={
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'account_type':'N',
        }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('profile')
        self.assertRedirects(response,redirect_url)

    ######################### delete_profile(request) ########################################
    def test_delete_profile_get_site(self):
        url = reverse('delete_profile')
        response = self.client.get(url+'?request_user_id={}'.format(self.test_user.id))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'profile_editing/delete_profile.html')

    def test_accept_to_delete_profile(self):
        url = reverse('delete_profile')
        response = self.client.post(url+'?request_user_id={}'.format(self.test_user.id))
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('register')
        self.assertRedirects(response,redirect_url)