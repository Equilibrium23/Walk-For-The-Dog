"""Walk_For_The_Dog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from register_and_login import views as register_and_login_views
from dog_editing import views as dog_editing_views
from profile_editing import views as profile_editing_views
from time_management import views as time_management_views
from users import views as users_views
from start_page import views as start_page_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls, name = "admin"),
    path('', start_page_views.start_page,name = "start_page"),
    path('accept/', start_page_views.accept, name = "accept"),
    path('decline/', start_page_views.decline, name = "decline"),
    path('login/', auth_views.LoginView.as_view(template_name='register_and_login/login.html'), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='register_and_login/logout.html'), name = "logout"),
    path('register/', register_and_login_views.register, name = "register"),
    path('profile/', users_views.profile, name = "profile"),
	path('chat/', users_views.chat, name = "chat"),
    path('calendar/', time_management_views.CalendarView.as_view(), name = "calendar"),
    path('add_dog/', dog_editing_views.add_dog, name = "add_dog"),
    path('update/', profile_editing_views.update, name = "update"),
    path('change_ac_type/', profile_editing_views.change_ac_type, name = "change_ac_type"),
    path('add_time_period/', time_management_views.add_time_period, name = "add_time_period"),
    path('edit_dog_profile/', dog_editing_views.edit_dog_profile, name = "edit_dog_profile"),
    path('delete_dog/', dog_editing_views.delete_dog, name = "delete_dog"),
    path('delete_profile/', profile_editing_views.delete_profile, name = "delete_profile"),
    path('calendar/synchronize/',time_management_views.synchronize_calendar,name="synchronize_calendar"),
    path('calendar/oauth2callback/',time_management_views.load_calendar_data,name="oauth2callback"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
