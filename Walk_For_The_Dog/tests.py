from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve

from register_and_login.views import register, add_dog, update, change_ac_type, add_time_period
from users.views import profile, CalendarView
from start_page.views import start_page
from django.contrib.auth import get_user_model


class TestUrls(SimpleTestCase):
    def test_start_page_is_resolved(self):
        url = reverse('start_page')
        self.assertEquals(resolve(url).func, start_page)

    def test_login_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_register_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profile_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_calendar_is_resolved(self):
        url = reverse('calendar')
        self.assertEquals(resolve(url).func.view_class, CalendarView)

    def test_add_dog_is_resolved(self):
        url = reverse('add_dog')
        self.assertEquals(resolve(url).func, add_dog)

    def test_add_update_is_resolved(self):
        url = reverse('update')
        self.assertEquals(resolve(url).func, update)

    def test_change_ac_type_is_resolved(self):
        url = reverse('change_ac_type')
        self.assertEquals(resolve(url).func, change_ac_type)
    
    def test_change_ac_type_is_resolved(self):
        url = reverse('add_time_period')
        self.assertEquals(resolve(url).func, add_time_period)


# # from django.contrib.auth import get_user_model
# # from django.contrib.auth.models import User
# register_data = {
#             'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
#             'username':'testing',
#             'name':'testing',
#             'email':'testing@testing.pl',
#             'password1':'pite12345678',
#             'password2':'pite12345678',
#             'account_type':'1',
#             'location':'Krakow',
#             'image':'',
#             'joining_date':'2020-12-18'
#         }
# class TestUrlResponse(TestCase):
#     # def test_register_get_site_response(self):
#     #     url = reverse('register')
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='get register request is invalid')
    
#     def test_register_post_data_response(self):
#         url = reverse('register')
#         response = self.client.post(url,register_data)
#         self.assertEquals(response.status_code, 302, msg ='post register request is invalid')
    
#     # def test_get_login_response(self):
#     #     url = reverse('login')
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='get login request is invalid')
    
#     # def test_post_login_response(self):
#     #     url = reverse('login')
#     #     login_data = {
#     #         'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
#     #         'username':'testing097',
#     #         'password':'pite12345678'
#     #     }
#     #     response = self.client.post(url,login_data)
#     #     self.assertEquals(response.status_code, 302, msg ='post login request is invalid')

#     # def test_logout_response(self):
#     #     url = reverse('logout')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='logout request is invalid')

#     # def test_profile_response(self):
#     #     url = reverse('profile')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='profile request is invalid')

#     # def test_calendar_response(self):
#     #     url = reverse('calendar')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='calendar request is invalid')

#     # def test_add_dog_response(self):
#     #     url = reverse('add_dog')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='add_dog request is invalid')

#     # def test_add_update_response(self):
#     #     url = reverse('update')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='update request is invalid')

#     # def test_change_ac_type_response(self):
#     #     url = reverse('change_ac_type')
#     #     self.client.login(username = register_data['username'], password = register_data['password1'])
#     #     response = self.client.get(url)
#     #     self.assertEquals(response.status_code, 200, msg ='change_ac_type request is invalid')
