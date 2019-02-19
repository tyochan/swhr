from django.test import TestCase
from django.urls import reverse_lazy

from personal_details.models import User
from leave_records.models import Leave
from leave_records import choices

import datetime
import json


class LeaveListViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com')
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK')
        self.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK')

        self.test_user2.slug = self.test_user2.staff_id

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()

        number_of_leaves = 8
        date = datetime.datetime.strptime('2019-1-31', '%Y-%m-%d').date()
        for obj in range(number_of_leaves):
            date = date + datetime.timedelta(days=1)
            day_type = 'FD'
            type = 'AL'
            status = 'PD'
            Leave.objects.create(
                user=self.test_user2,
                start_date=date,
                end_date=date,
                spend=1,
                day_type=day_type,
                type=type,
                status=status,
            )
            Leave.objects.create(
                user=self.test_user3,
                start_date=date,
                end_date=date,
                spend=1,
                day_type=day_type,
                type=type,
                status=status,
            )

        for obj in range(number_of_leaves):
            date = date + datetime.timedelta(days=1)
            day_type = 'HD'
            type = 'SL'
            status = 'RE'
            Leave.objects.create(
                user=self.test_user2,
                start_date=date,
                end_date=date,
                spend=1,
                day_type=day_type,
                type=type,
                status=status,
            )
            Leave.objects.create(
                user=self.test_user3,
                start_date=date,
                end_date=date,
                spend=1,
                day_type=day_type,
                type=type,
                status=status,
            )

    def test_redirects_if_not_logged_in(self):
        response = self.client.get(reverse_lazy('leave_records:index'))
        self.assertRedirects(response, '/login/?next=/leave_records/')

    def test_logged_in_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leave_records.html')

    def test_logged_in_get_extra_context_data(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:index'))

        # Check default context data for filtering and sorting
        self.assertEqual(response.context['order_by'], '-end_date')
        self.assertEqual(response.context['staff_id'], '')
        self.assertEqual(response.context['name'], '')
        self.assertEqual(response.context['type'], '')
        self.assertEqual(response.context['day_type'], '')
        self.assertEqual(response.context['status'], '')
        self.assertEqual(
            response.context['type_options'],
            dict((key, val) for key, val in choices.LEAVE_TYPE))
        self.assertEqual(
            response.context['status_options'],
            dict((key, val) for key, val in choices.STATUS_CHOICES))
        self.assertEqual(
            response.context['day_type_options'],
            dict((key, val)for key, val in choices.LEAVE_DAY_TYPE))
        self.assertEqual(
            response.context['filter'],
            'staff_id=%s&name=%s&type=%s&day_type=%s&status=%s' % (
                response.context['staff_id'], response.context['name'],
                response.context['type'], response.context['day_type'],
                response.context['status']
            )
        )

    def test_pagination_is_13(self):
        self.client.login(username='testuser3', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['obj_list']) == 13)

    def test_lists_all_objects_if_logged_in_as_superuser(self):
        # Get second page and confirm it has (exactly) remaining items
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'leave_records:index') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['obj_list']) == 6)

    def test_lists_own_objects_if_logged_in(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:index'))

        for obj in response.context['obj_list']:
            self.assertTrue(obj.user.username == 'testuser2')

    def test_pages_ordered_by_desc_end_date(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:index'))

        last_date = 0
        for obj in response.context['obj_list']:
            if last_date == 0:
                last_date = obj.end_date
            else:
                self.assertTrue(last_date > obj.end_date)
                last_date = obj.end_date

    def test_pages_ordered_by_desc_start_date(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse_lazy('leave_records:index'),
            {'order_by': '-start_date'}
        )

        last_date = 0
        for obj in response.context['obj_list']:
            if last_date == 0:
                last_date = obj.start_date
            else:
                self.assertTrue(last_date > obj.start_date)
                last_date = obj.start_date

    def test_object_queryset_filter_by_staff_id(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse_lazy('leave_records:index'),
            {'staff_id': self.test_user2.slug}
        )
        for obj in response.context['obj_list']:
            self.assertTrue(obj.user.username == 'testuser2')


class LeaveModifyViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com')
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK', annual_leave=15.0)
        self.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK', annual_leave=15.0)

        self.test_user2.slug = self.test_user2.staff_id

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()

        date = datetime.datetime.strptime('2019-1-31', '%Y-%m-%d').date()
        status = 'PD'
        Leave.objects.create(
            user=self.test_user2,
            start_date=date,
            end_date=date + datetime.timedelta(days=8),
            spend=3,
            day_type='FD',
            type='AL',
            status=status,
        )
        for i in range(2):
            Leave.objects.create(
                user=self.test_user3,
                start_date=date + datetime.timedelta(days=1),
                end_date=date + datetime.timedelta(days=1),
                spend=0.5,
                day_type='HD',
                type='AL',
                status=status,
            )

    ### LeaveCreateViewTest ###
    def test_redirects_if_not_logged_in_LeaveCreateViewTest(self):
        response = self.client.get(reverse_lazy('leave_records:create_leave'))
        self.assertRedirects(response, '/login/?next=/leave_records/create/')

    def test_logged_in_url_exists_at_desired_location_LeaveCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/create/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LeaveCreateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:create_leave'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_leave.html')

    def test_form_has_kwargs_user_LeaveCreateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:create_leave'))
        self.assertEquals(response.context['form'].user, self.test_user2)

    def test_create_leave_success_full_day(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse_lazy('leave_records:create_leave'),
            {
                'user': self.test_user2.id,
                'start_date': datetime.datetime.strptime('2019-2-11', '%Y-%m-%d').date(),
                'end_date': datetime.datetime.strptime('2019-2-15', '%Y-%m-%d').date(),
                'spend': 5,
                'day_type': 'FD',
                'type': 'AL',
            })
        # Call object again due to change
        annual_leave = User.objects.get(username='testuser2').annual_leave
        self.assertEquals(annual_leave, 10)

    def test_create_leave_success_half_day(self):
        self.client.login(username='testuser3', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-18', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('leave_records:create_leave'),
            {
                'user': self.test_user3.id,
                'start_date': date,
                'end_date': date,
                'spend': 0.5,
                'day_type': 'HD',
                'type': 'AL',
            })
        # Call object again due to change
        reverse_lazy('leave_records:index')
        annual_leave = User.objects.get(username='testuser3').annual_leave
        self.assertEquals(annual_leave, 14.5)

    def test_create_leave_fail_spend_exceeds_quota(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse_lazy('leave_records:create_leave'),
            {
                'user': self.test_user2.id,
                'start_date': datetime.datetime.strptime('2019-2-11', '%Y-%m-%d').date(),
                'end_date': datetime.datetime.strptime('2019-2-15', '%Y-%m-%d').date(),
                'spend': 100,
                'day_type': 'FD',
                'type': 'AL',
            })
        self.assertEqual(response.status_code, 200)
        msg = f'Leave exceeds current quota of {self.test_user2.annual_leave} days.'
        self.assertFormError(response, 'form', None, msg)

    def test_create_leave_fail_half_day_leaves_exist(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('leave_records:create_leave'),
            {
                'user': self.test_user3.id,
                'start_date': date,
                'end_date': date,
                'spend': 5,
                'day_type': 'HD',
                'type': 'AL',
            })
        self.assertEqual(response.status_code, 200)
        msg = f'Leaves have been taken for {date}'
        self.assertFormError(response, 'form', None, msg)

    def test_create_leave_fail_overlapping_leave_exists(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('leave_records:create_leave'),
            {
                'user': self.test_user3.id,
                'start_date': date,
                'end_date': date + datetime.timedelta(days=1),
                'spend': 5,
                'day_type': 'FD',
                'type': 'AL',
            })
        self.assertEqual(response.status_code, 200)
        obj = Leave.objects.filter(
            user=self.test_user3, start_date=date).first()
        msg = f'Leave overlapping with {obj}'
        self.assertFormError(response, 'form', None, msg)

    ### LeaveUpdateViewTest ###
    def test_redirects_if_not_logged_in_LeaveUpdateViewTest(self):
        response = self.client.get('/leave_records/update/1/')
        self.assertRedirects(response, '/login/?next=/leave_records/update/1/')

    def test_forbidden_if_not_superuser_LeaveUpdateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/update/1/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LeaveUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/update/1/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LeaveUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:update_leave',
                                                kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_leave.html')

    def test_form_has_kwargs_user_LeaveUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/update/1/')
        self.assertEquals(response.context['form'].user, self.test_user1)

    def test_update_leave_success_reject(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-1-31', '%Y-%m-%d').date()
        response = self.client.post(
            '/leave_records/update/1/',
            {
                'user': self.test_user2.id,
                'start_date': date,
                'end_date': date + datetime.timedelta(days=8),
                'spend': 3,
                'day_type': 'FD',
                'type': 'AL',
                'status': 'PD',
                'reject': 'reject',
            })
        # Call object again due to change
        self.assertRedirects(response, reverse_lazy('leave_records:index'))

        leave = Leave.objects.get(user=self.test_user2, start_date=date)
        self.assertEquals(leave.status, 'RE')
        annual_leave = User.objects.get(username='testuser2').annual_leave
        self.assertEquals(annual_leave, 18)

    def test_update_leave_success_approve(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-1-31', '%Y-%m-%d').date()
        response = self.client.post(
            '/leave_records/update/1/',
            {
                'user': self.test_user2.id,
                'start_date': date,
                'end_date': date + datetime.timedelta(days=8),
                'spend': 3,
                'day_type': 'FD',
                'type': 'AL',
                'status': 'PD',
                'approve': 'approve',
            })
        # Call object again due to change
        self.assertRedirects(response, reverse_lazy('leave_records:index'))

        leave = Leave.objects.get(user=self.test_user2, start_date=date)
        self.assertEquals(leave.status, 'AP')
        annual_leave = User.objects.get(username='testuser2').annual_leave
        self.assertEquals(annual_leave, 15)

    ### LeaveDetailViewTest ###
    def test_redirects_if_not_logged_in_LeaveDetailViewTest(self):
        response = self.client.get('/leave_records/detail/1/')
        self.assertRedirects(response, '/login/?next=/leave_records/detail/1/')

    def test_forbidden_if_not_superuser_and_owne_LeaveDetailViewTestr(self):
        self.client.login(username='testuser3', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/detail/1/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LeaveDetailViewTest(self):
        # Test with superuser
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LeaveDetailViewTest(self):
        # Test with owner
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('leave_records:detail_leave',
                                                kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_leave.html')

    def test_form_has_kwargs_user_LeaveDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/leave_records/detail/1/')
        self.assertEquals(response.context['form'].user, self.test_user1)

    def test_redirects_for_any_data_posting(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-1-31', '%Y-%m-%d').date()
        response = self.client.post(
            '/leave_records/detail/1/',
            {
                'user': self.test_user2.id,
                'start_date': date,
                'end_date': date + datetime.timedelta(days=8),
                'spend': 3,
                'day_type': 'FD',
                'type': 'AL',
                'status': 'AP',
            })
        self.assertRedirects(response, reverse_lazy('leave_records:index'))

    ### Leave Calculation ###
    def test_leave_calculation_more_than_one_day(self):
        response = self.client.get(
            '/leave_records/ajax/leave_calculation',
            data={
                'start_date': '2019-2-1',
                'end_date': '2019-2-8'
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        decoded_json = json.loads(response.content)
        self.assertEquals(decoded_json['content']['days_spend'], 3)

    def test_leave_calculation_broken_period(self):
        response = self.client.get(
            '/leave_records/ajax/leave_calculation',
            data={
                'start_date': '2019-2-9',
                'end_date': '2019-2-8'
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        decoded_json = json.loads(response.content)
        self.assertEquals(decoded_json['content']['days_spend'], 0)

    def test_leave_calculation_half_day(self):
        response = self.client.get(
            '/leave_records/ajax/leave_calculation',
            data={
                'start_date': '2019-2-8',
                'end_date': '2019-2-8',
                'day_type': 'HD'
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        decoded_json = json.loads(response.content)
        self.assertEquals(decoded_json['content']['days_spend'], 0.5)

    def test_leave_calculation_one_day(self):
        response = self.client.get(
            '/leave_records/ajax/leave_calculation',
            data={
                'start_date': '2019-2-8',
                'end_date': '2019-2-8',
                'day_type': 'FD'
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        decoded_json = json.loads(response.content)
        self.assertEquals(decoded_json['content']['days_spend'], 1)
