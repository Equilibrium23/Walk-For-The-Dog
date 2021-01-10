from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import TimePeriod
from register_and_login.models import Profile
from datetime import datetime,date,time
from .utils import hourly_it, number_of_rows, Calendar


class TestTimeManagementViewsAndUtils(TestCase):
    def setUp(self):
        self.test_username = 'test'
        self.test_password = 'test'
        self.test_user = User.objects.create_user(username=self.test_username, password=self.test_password)
        self.test_user.save()
        self.client.login(username='test', password='test')

    def test_add_time_period_get_site(self):
        url = reverse('add_time_period')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'time_management/add_time_period.html')

    def test_add_time_period_data_posted(self):
        url = reverse('add_time_period')
        add_period_data = {
            'csrfmiddlewaretoken':'TtGVEhVsVewJkhI9vRFE0rUus4KPhbRw8KCpz8ZPXu15S2Jp5uuihn31tGwPoZ5P',
            'day':date(2021, 1, 7),
            'start_hour':time(6, 0),
            'time_length':time(6, 30),
            'dogs_choice':''
        }
        response = self.client.post(url, add_period_data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'time_management/add_time_period.html')


    def test_hourly_it(self):
        starthour = datetime(year=2020, month=12, day=11, hour=5, minute=0)
        finishhour = datetime(year=2020, month=12, day=11, hour=23, minute=0)
        compare = datetime(year=2020, month=12, day=11, hour=5, minute=30)

        x = hourly_it(starthour, finishhour, 30)
        self.assertEquals(next(x), compare)

    def test_number_of_rows(self):
        starthour = datetime(year=2020, month=12, day=11, hour=5, minute=0)
        finishhour = datetime(year=2020, month=12, day=11, hour=6, minute=0)
        compare = 3
        x = number_of_rows(starthour, finishhour)
        self.assertEquals(x, compare)

    def test_formatweekheader(self):
        calendar = Calendar()
        result = calendar.formatweekheader()
        self.assertEquals(result,'''<thead class="font-weight-bold text-uppercase"><tr><th span="col"> Mon </th><th span="col"> Tue </th><th span="col"> Wed </th><th span="col"> Thu </th><th span="col"> Fri </th><th span="col"> Sat </th><th span="col"> Sun </th></tr></thead>''')

    def test_formatweekheaderforweek(self):
        starthour = datetime(year=2020, month=12, day=11, hour=5, minute=0)
        calendar = Calendar()
        result = calendar.formatweekheaderforweek(starthour)
        self.assertEquals(result,'''<thead><tr class="text-uppercase"><th span="col">time</th><th span="col"><a href="../calendar/?view=day&date=2020-12-11"> Mon 11 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-12"> Tue 12 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-13"> Wed 13 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-14"> Thu 14 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-15"> Fri 15 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-16"> Sat 16 </a></th>
<th span="col"><a href="../calendar/?view=day&date=2020-12-17"> Sun 17 </a></th>
</tr></thead>''')

    def test_formatmonth(self):
        d = datetime.now()
        calendar = Calendar(d.year, d.month, d.day)
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 7), start_hour=time(6, 30),
                                  end_hour=time(7, 00))
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 7), start_hour=time(8, 30),
                                  end_hour=time(9, 00))

        events = TimePeriod.objects.filter(person=self.test_user)
        result = calendar.formatmonth(events)
        self.assertTrue('''<div class="bg-success"> 08:30-09:00: free time</div>''' in result)
        self.assertTrue('''<div class="bg-success"> 06:30-07:00: free time</div>''' in result)

    def test_formatbyweek(self):
        calendar = Calendar(2021, 1, 9)
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 10), start_hour=time(6, 30),
                                  end_hour=time(7, 00))
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 10), start_hour=time(8, 30),
                                  end_hour=time(9, 00))
        events = TimePeriod.objects.filter(person=self.test_user)

        result = calendar.formatbyweek(events)
        self.assertTrue('''<tr><th scope="row">06:30</th><td></td><td></td><td></td><td></td><td></td><td></td><td rowspan="2" class="bg-success"> free time </td></tr>''' in result)
        self.assertTrue('''<tr><th scope="row">08:30</th><td></td><td></td><td></td><td></td><td></td><td></td><td rowspan="2" class="bg-success"> free time </td></tr>''' in result)

    def test_formatbyday(self):
        calendar = Calendar(2021, 1, 9)
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 7), start_hour=time(6, 30),
                                  end_hour=time(7, 00))
        TimePeriod.objects.create(person=self.test_user, day=date(2021, 1, 7), start_hour=time(8, 30),
                                  end_hour=time(9, 00))
        events = TimePeriod.objects.filter(person=self.test_user)

        result = calendar.formatbyday(events)
        self.assertTrue('''Saturday, 09 Jan 2021''' in result)
        calendar = Calendar(2021, 1, 7)
        result = calendar.formatbyday(events)
        self.assertTrue('''<tr><th scope="row">06:30</th><td rowspan="2" class="bg-success"> free time </td></tr>''' in result)

