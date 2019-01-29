from django.test import TestCase
from .models import User

# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '123456'


class UserTest(TestCase):
    def create_user(self):
        return User.objects.create(
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
        )

    def test_user_creation(self):
        obj = self.create_user()
        self.assertTrue(isinstance(obj, User))
        print('Class: ', obj.__class__.__name__)

        self.assertEqual(obj.__str__(), '%s %s %s' %
                         (obj.staff_id, obj.last_name, obj.first_name))
        print('Get Display: ', obj.__str__())

        self.assertEqual(obj.get_name(), '%s %s' %
                         (obj.last_name, obj.first_name))
        print('Get Name: ', obj.get_name())

    def test_index(self):
        resp = self.client.get('/personal_details/')
        self.assertEqual(resp.status_code, 200)
