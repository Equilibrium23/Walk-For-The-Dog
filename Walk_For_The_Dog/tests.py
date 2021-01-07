################## django stuff ###############################
from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib import admin
###############################################################

#######################################################################################
from register_and_login.views import register
from users.views import profile,chat
from time_management.views import CalendarView,add_time_period,synchronize_calendar
from dog_editing.views import add_dog,edit_dog_profile,delete_dog
from profile_editing.views import update,change_ac_type,delete_profile
from start_page.views import start_page
#######################################################################################

class TestUrls(SimpleTestCase):

    def test_start_page_is_resolved(self):
        url = reverse('')
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

    def test_chat_is_resolved(self):
        url = reverse('chat')
        self.assertEquals(resolve(url).func, chat)

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
    
    def test_add_time_period_is_resolved(self):
        url = reverse('add_time_period')
        self.assertEquals(resolve(url).func, add_time_period)

    def test_edit_dog_profile_is_resolved(self):
        url = reverse('edit_dog_profile')
        self.assertEquals(resolve(url).func, edit_dog_profile)
    
    def test_delete_dog_is_resolved(self):
        url = reverse('delete_dog')
        self.assertEquals(resolve(url).func, delete_dog)
    
    def test_delete_profile_is_resolved(self):
        url = reverse('delete_profile')
        self.assertEquals(resolve(url).func, delete_profile)
    
    def test_synchronize_calendar_is_resolved(self):
        url = reverse('synchronize_calendar')
        self.assertEquals(resolve(url).func, synchronize_calendar)
