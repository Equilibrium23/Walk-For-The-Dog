from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
register_data = {
    'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
    'username':'testing',
    'name':'testing',
    'email':'testing@testing.pl',
    'password1':'pite12345678',
    'password2':'pite12345678',
    'account_type':'N',
    'location':'Krakow',
    'image':'',
    'joining_date':'2020-12-18'
}

class TestRegisterAndLoginViews(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        user = User.objects.create_user(username=self.test_username, password=self.test_password)
        user.save()
##################### register ######################################################
    def test_register_get_site_response(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200, msg ='get register request is invalid')
        
    def test_register_good_data_response(self):
        url = reverse('register')
        response = self.client.post(url,register_data)
        self.assertEquals(response.status_code, 302, msg ='post register request is invalid')
        self.assertRedirects(response,'/login/')
    
    def test_register_bad_data_response(self):
        url = reverse('register')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200, msg ='post register request is invalid')
    
    def test_register_bad_data_used_template(self):
        url = reverse('register')
        response = self.client.post(url)
        self.assertTemplateUsed(response,'register_and_login/register.html')
##################### login ######################################################
    def test_login_used_template(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertTemplateUsed(response,'register_and_login/login.html')
        
    def test_login_bad_data_response(self):
        url = reverse('login')
        login_data = {
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'username':'',
            'password':'',
        }
        response = self.client.post(url, login_data)
        self.assertEquals(response.status_code, 200, msg ='post login request is invalid')
        self.assertTemplateUsed(response,'register_and_login/login.html')

    
    def test_login_good_data_response(self):
        url = reverse('login')
        login_data = {
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'username':self.test_username,
            'password':self.test_password,
        }
        response = self.client.post(url, login_data)
        self.assertEquals(response.status_code, 302, msg ='post login request is invalid')
        redirect_url = reverse('start_page')
        self.assertRedirects(response,redirect_url)
