from django.contrib.auth.views import LoginView, LogoutView
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from register_and_login.views import register, add_dog, update, change_ac_type
from users.views import profile, CalendarView


class TestUrls(SimpleTestCase):
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

