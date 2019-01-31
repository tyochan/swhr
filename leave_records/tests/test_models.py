from django.test import TestCase
from personal_details.models import User
from leave_records.models import Leave

# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '234561'
username = '123456'
password = '123456'
date = '2019-1-1'
salary = 20000
string = 'Testing'


class LeaveModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
            username=username,
            password=password,
            slug=staff_id,
        )
        Leave.objects.create(
            user=cls.user,
            start_date=date,
            end_date=date,
            spend=1,
        )

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    def test_get_absolute_url(self):
        obj = Leave.objects.get(user=self.user, start_date=date)
        self.assertEquals(obj.get_absolute_url(), '/leave_records/')

    def test_str(self):
        obj = Leave.objects.get(user=self.user, start_date=date)
        expected_result = f'{obj.user.get_name()}: {obj.get_status_display()} {obj.get_type_display()} from {obj.start_date.strftime("%Y/%m/%d")} to {obj.end_date.strftime("%Y/%m/%d")} as {obj.spend} days'
        self.assertEquals(str(obj), expected_result)
