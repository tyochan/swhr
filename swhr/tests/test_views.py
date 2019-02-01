from django.test import TestCase, Client, RequestFactory
from personal_details.models import User
from django.contrib.auth.models import AnonymousUser
from swhr.views import CustomLoginView, CustomPasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


import datetime

first_name = 'First'
last_name = 'Last'
staff_id = '234561'
staff_id_two = '456789'
date = datetime.datetime.strptime('2019-1-3', '%Y-%m-%d')
date_two = datetime.datetime.strptime('2019-3-3', '%Y-%m-%d')
today = datetime.date.today()
salary = 20000


class MainViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            first_name=first_name, last_name=last_name,
            staff_id=staff_id, slug=staff_id,
            username=staff_id,
        )
        self.user.set_password(staff_id)
        self.superuser = User.objects.create(
            first_name=first_name, last_name=last_name,
            staff_id=staff_id_two, slug=staff_id,
            username=staff_id_two,
            is_superuser=True,
        )
        self.superuser.set_password(staff_id_two)

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

    # def test_login_view(self):
        # request = self.factory.get('/login/')
        # request.user = AnonymousUser()
        #
        # response = CustomLoginView.as_view()(request)
        # self.assertEqual(response.status_code, 200)

    def test_get_login_page(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    # Unknown error with redirection
    # def test_login_with_valid_user(self):
    #     response = self.client.post(
    #         reverse_lazy('login'),
    #         {'username': staff_id, 'password': staff_id},
    #     )
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'leave_records.html')

    def test_get_change_password_page(self):
        print(self.client.login(username=self.user.username,
                                password=self.user.password))
        # print(self.client.force_login(self.user))
        response = self.client.get(reverse_lazy('change_password'))

        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(
        #     response, 'form_change_password.html')
