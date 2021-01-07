from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Dog
from register_and_login.models import Profile


# przed
# dog_editing/__init__.py                          0      0   100%
# dog_editing/admin.py                             3      0   100%
# dog_editing/apps.py                              3      0   100%
# dog_editing/forms.py                            11      0   100%
# dog_editing/migrations/0001_initial.py           6      0   100%
# dog_editing/migrations/__init__.py               0      0   100%
# dog_editing/models.py                           15      1    93%
# dog_editing/tests.py                             1      0   100%
# dog_editing/views.py                            50     37    26%

class TestDogEditingViews(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        test_user.save()
        self.client.login(username='test', password='test')
        # dog_owner = Profile.objects.create( user = test_user, name = self.test_username )
        # Dog.objects.create(DOG_SIZE = 'S',dog_name='test', breed='kundel',short_description = 'piekny pies',image='',owner = dog_owner )
        # test_dog = Dog.objects.get(name="test")
        # self.test_dog_id = test_dog.id

    ######################### add_dog(request) ########################################
    def test_add_dog_get_site(self):
        url = reverse('add_dog')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'dog_editing/add_dog.html')
    
    def test_add_dog_bad_data_posted(self):
        url = reverse('add_dog')
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'dog_editing/add_dog.html')
    
    def test_add_dog_good_data_posted(self):
        url = reverse('add_dog')
        add_dog_data = {
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'dog_name':'azor',
            'breed':'kundel',
            'size':'S',
            'short_description':'piekny pies',
            'image':''
        }
        response = self.client.post(url,add_dog_data)
        self.assertEquals(response.status_code, 302)
        redirect_url = reverse('profile')
        self.assertRedirects(response,redirect_url)
    ######################### edit_dog_profile(request) ########################################
    # def test_edit_dog_profile_get_site(self):
    #     url = reverse('edit_dog_profile')
    #     response = self.client.get(url,{'request_dog_id':self.dog_id})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response,'dog_editing/edit_dog_profile.html')
    
    # def test_add_dog_bad_data_posted(self):
    #     url = reverse('edit_dog_profile')
    #     response = self.client.post(url+"?request_dog_id="+self.dog_id)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response,'dog_editing/edit_dog_profile.html')
    
    # def test_add_dog_good_data_posted(self):
    #     url = reverse('edit_dog_profile')
    #     edit_dog_data = {
    #         'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
    #         'dog_name':'azor',
    #         'breed':'kundel',
    #         'size':'S',
    #         'short_description':'piekny pies',
    #         'image':''
    #     }
    #     response = self.client.post(url+"?request_dog_id="+self.dog_id,edit_dog_data)
    #     self.assertEquals(response.status_code, 302)
    #     self.assertTemplateUsed(response,'dog_editing/add_dog.html')