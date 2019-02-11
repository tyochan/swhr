from django.test import TestCase
from personal_details.models import User
from django.urls import reverse_lazy

import datetime


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com')
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')

        self.test_user2.slug = self.test_user2.staff_id
        self.test_user1.save()
        self.test_user2.save()

    def test_url_exists_at_desired_location_and_uses_correct_template(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_url_accessible_by_name_and_uses_correct_template(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'testuser1',
                'password': '1X<ISRUkw+tuK',
            }
        )
        self.assertRedirects(response, reverse_lazy('leave_records:index'))

    def test_login_fail(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'testuser1',
                'password': '1X<ISRUkw+tuL',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_redirects_if_logged_in(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/login/')
        self.assertRedirects(response, reverse_lazy('leave_records:index'))

    ### PasswordChangeViewTest ###
    def test_url_exists_at_desired_location_and_uses_correct_template(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/change_password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_change_password.html')

    def test_url_accessible_by_name_and_uses_correct_template(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('change_password'))
        self.assertEqual(response.status_code, 200)

    def test_redirects_if_not_logged_in(self):
        response = self.client.get('/change_password/')
        self.assertRedirects(response, '/login/?next=/change_password/')

    def test_redirects_after_password_change(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.post(
            '/change_password/',
            {
                'old_password': '1X<ISRUkw+tuK',
                'new_password1': '1X<ISRUkw+tuH',
                'new_password2': '1X<ISRUkw+tuH'
            }
        )
        self.assertRedirects(
            response,
            reverse_lazy('personal_details:update_user',
                         kwargs={'slug': self.test_user2.slug})
        )
