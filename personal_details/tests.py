from django.test import TestCase
from .models import User

# Create your tests here.


class UserTest(TestCase):
    def create_user(self, first_name='First', last_name='Last'):
        return User.objects.create(first_name=first_name, last_name=last_name)

    def test_user_creation(self):
        obj = self.create_user()
        self.assertTrue(isinstance(obj, User))
        self.assertEqual(obj.__str__(), '%s %s %s' %
                         (obj.staff_id, obj.last_name, obj.first_name))
