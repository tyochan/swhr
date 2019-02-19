from django.test import TestCase
from django.urls import reverse_lazy

from personal_details.models import User
from leave_records.models import Leave
from payroll.models import Payment
from payroll import choices

import datetime


class PaymentListViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com', salary=50000)
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK', salary=7000)

        self.test_user2.slug = self.test_user2.staff_id

        self.test_user1.save()
        self.test_user2.save()

        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        for i in range(13):
            Payment.objects.create(
                user=self.test_user1,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user1.salary,
                total_payments=self.test_user1.salary,
                np_leave=0,
                total_deductions=self.test_user1.salary * 0.05,
                mpf_employer=self.test_user1.salary * 0.05,
                mpf_employee=self.test_user1.salary * 0.05,
                net_pay=self.test_user1.salary * 0.95,
                is_last=True
            )
        for i in range(2):
            Payment.objects.create(
                user=self.test_user2,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user2.salary,
                total_payments=self.test_user2.salary,
                np_leave=0,
                total_deductions=self.test_user2.salary * 0.05,
                mpf_employer=self.test_user2.salary * 0.05,
                mpf_employee=0,
                net_pay=self.test_user2.salary,
            )
            date = date.replace(month=date.month + 1)

    def test_redirects_if_not_logged_in_PaymentListViewTest(self):
        response = self.client.get(reverse_lazy('payroll:index'))
        self.assertRedirects(response, '/login/?next=/payroll/')

    def test_logged_in_url_exists_at_desired_location_PaymentListViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_PaymentListViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payroll.html')

    def test_logged_in_get_extra_context_data_PaymentListViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:index'))

        # Check default context data for filtering and sorting
        self.assertEqual(response.context['order_by'], '-period_start')
        self.assertEqual(response.context['staff_id'], '')
        self.assertEqual(response.context['name'], '')
        self.assertEqual(response.context['status'], '')
        self.assertEqual(response.context['is_last'], '')
        self.assertEqual(
            response.context['is_last_options'],
            dict({'': 'Monthly Payment', 'True': 'Last Payment'}))
        self.assertEqual(
            response.context['status_options'],
            dict((key, val) for key, val in choices.STATUS_CHOICES))
        self.assertEqual(
            response.context['filter'],
            'staff_id=%s&name=%s&status=%s&is_last=%s' % (
                response.context['staff_id'], response.context['name'],
                response.context['is_last'], response.context['status']
            )
        )

    def test_pagination_is_13_PaymentListViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['obj_list']) == 13)

    def test_lists_all_objects_if_logged_in_as_superuser_PaymentListViewTest(self):
        # Get second page and confirm it has (exactly) remaining items
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['obj_list']) == 2)

    def test_lists_own_objects_if_logged_in_PaymentListViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:index'))

        for obj in response.context['obj_list']:
            self.assertTrue(obj.user.username == 'testuser2')

    def test_pages_ordered_by_desc_period_start_PaymentListViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:index'))

        last_date = 0
        for obj in response.context['obj_list']:
            if last_date == 0:
                last_date = obj.period_start
            else:
                self.assertTrue(last_date > obj.period_start)
                last_date = obj.period_start

    def test_pages_ordered_by_desc_start_date_PaymentListViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse_lazy('payroll:index'),
            {'order_by': '-period_end'}
        )

        last_date = 0
        for obj in response.context['obj_list']:
            if last_date == 0:
                last_date = obj.period_end
            else:
                self.assertTrue(last_date > obj.period_end)
                last_date = obj.period_end

    def test_object_queryset_filter_by_staff_id_PaymentListViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse_lazy('payroll:index'),
            {'staff_id': self.test_user2.slug}
        )
        for obj in response.context['obj_list']:
            self.assertTrue(obj.user.username == 'testuser2')


class PaymentModifyViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com', salary=50000)
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK', salary=7000)
        self.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK', salary=18550)
        self.test_user4 = User.objects.create_user(
            username='testuser4', password='1X<ISRUkw+tuK', salary=31000)

        self.test_user2.slug = self.test_user2.staff_id
        self.test_user3.slug = self.test_user3.staff_id
        self.test_user4.slug = self.test_user4.staff_id

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()
        self.test_user4.save()

        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        for i in range(2):
            Payment.objects.create(
                user=self.test_user1,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user2.salary,
                total_payments=self.test_user2.salary,
                np_leave=0,
                total_deductions=self.test_user2.salary * 0.05,
                mpf_employer=self.test_user2.salary * 0.05,
                mpf_employee=0,
                net_pay=self.test_user2.salary,
                status='CC',
            )
            Payment.objects.create(
                user=self.test_user2,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user2.salary,
                total_payments=self.test_user2.salary,
                np_leave=0,
                total_deductions=self.test_user2.salary * 0.05,
                mpf_employer=self.test_user2.salary * 0.05,
                mpf_employee=0,
                net_pay=self.test_user2.salary,
                status='PA',
            )
            Payment.objects.create(
                user=self.test_user3,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user3.salary,
                total_payments=self.test_user3.salary,
                np_leave=0,
                total_deductions=self.test_user3.salary * 0.05,
                mpf_employer=self.test_user3.salary * 0.05,
                mpf_employee=self.test_user3.salary * 0.05,
                net_pay=self.test_user3.salary * 0.95,
                status='PA',
            )
            Payment.objects.create(
                user=self.test_user4,
                period_start=date,
                period_end=date,
                pay_date=date,
                basic_salary=self.test_user4.salary,
                total_payments=self.test_user4.salary,
                np_leave=0,
                total_deductions=self.test_user4.salary - 1500,
                mpf_employer=1500,
                mpf_employee=1500,
                net_pay=self.test_user4.salary - 1500,
                status='PA',
            )
            date = date.replace(month=date.month + 1)

    ### PaymentCreateViewTest ###
    def test_redirects_if_not_logged_in_PaymentCreateViewTest(self):
        response = self.client.get(reverse_lazy('payroll:create_payment'))
        self.assertRedirects(response, '/login/?next=/payroll/create/')

    def test_forbidden_if_not_superuser_PaymentCreateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/create/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_PaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/create/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_PaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:create_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    def test_redirects_if_create_payment_success_PaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-10-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('payroll:create_payment'),
            {
                'user': self.test_user2.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
            })
        self.assertRedirects(response, reverse_lazy('payroll:index'))
        obj_exists = True if Payment.objects.get(
            user=self.test_user2, period_start=date) else False
        self.assertTrue(obj_exists)

    def test_create_payment_fail_overlapping_date_PaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('payroll:create_payment'),
            data={
                'user': self.test_user2.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
            })
        self.assertEqual(response.status_code, 200)
        payment = Payment.objects.filter(user=self.test_user2,
                                         period_start__lte=date,
                                         period_end__gte=date
                                         ).exclude(status="CC").first()
        msg = f'Payment overlapping with {payment}'
        self.assertFormError(response, 'form', None, msg)

    ### PaymentUpdateViewTest ###
    def test_redirects_if_not_logged_in_PaymentUpdateViewTest(self):
        response = self.client.get('/payroll/update/1/')
        self.assertRedirects(response, '/login/?next=/payroll/update/1/')

    def test_forbidden_if_not_superuser_PaymentUpdateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/update/6/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_PaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/update/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_PaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:update_payment', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    def test_redirects_after_update_payment_success_PaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        response = self.client.post(
            '/payroll/update/4/',
            data={
                'user': self.test_user4.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
                'cancel': 'cancel',
            })
        self.assertRedirects(response, reverse_lazy('payroll:index'))
        status = Payment.objects.get(
            user=self.test_user4, period_start=date).status
        self.assertEquals(status, 'CC')

    ### PaymentDetailViewTest ###
    def test_redirects_if_not_logged_in_PaymentDetailViewTest(self):
        response = self.client.get('/payroll/detail/2/')
        self.assertRedirects(response, '/login/?next=/payroll/detail/2/')

    def test_forbidden_if_not_superuser_PaymentDetailViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/detail/2/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_PaymentDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/detail/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_PaymentDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:detail_payment', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    ### PaymentPDFViewTest ###
    def test_redirects_if_not_logged_in_PaymentPDFViewTest(self):
        response = self.client.get('/payroll/payslipPDF/2/')
        self.assertRedirects(response, '/login/?next=/payroll/payslipPDF/2/')

    def test_forbidden_if_not_superuser_and_owner_PaymentPDFViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/payslipPDF/4/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_PaymentPDFViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/payslipPDF/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_PaymentPDFViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:payslip_pdf', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payslip_pdf.html')


class LastPaymentModifyViewTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com', salary=50000)
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK', salary=7000)
        self.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK', salary=18550)
        self.test_user4 = User.objects.create_user(
            username='testuser4', password='1X<ISRUkw+tuK', salary=31000)

        self.test_user2.slug = self.test_user2.staff_id
        self.test_user3.slug = self.test_user3.staff_id
        self.test_user4.slug = self.test_user4.staff_id

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()
        self.test_user4.save()

        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        Payment.objects.create(
            user=self.test_user1,
            period_start=date,
            period_end=date,
            pay_date=date,
            basic_salary=self.test_user2.salary,
            total_payments=self.test_user2.salary,
            np_leave=0,
            total_deductions=self.test_user2.salary * 0.05,
            mpf_employer=self.test_user2.salary * 0.05,
            mpf_employee=0,
            net_pay=self.test_user2.salary,
            status='CC',
            is_last=True,
        )
        Payment.objects.create(
            user=self.test_user2,
            period_start=date,
            period_end=date,
            pay_date=date,
            basic_salary=self.test_user2.salary,
            total_payments=self.test_user2.salary,
            np_leave=0,
            total_deductions=self.test_user2.salary * 0.05,
            mpf_employer=self.test_user2.salary * 0.05,
            mpf_employee=0,
            net_pay=self.test_user2.salary,
            status='PA',
            is_last=True,
        )
        Payment.objects.create(
            user=self.test_user3,
            period_start=date,
            period_end=date,
            pay_date=date,
            basic_salary=self.test_user3.salary,
            total_payments=self.test_user3.salary,
            np_leave=0,
            total_deductions=self.test_user3.salary * 0.05,
            mpf_employer=self.test_user3.salary * 0.05,
            mpf_employee=self.test_user3.salary * 0.05,
            net_pay=self.test_user3.salary * 0.95,
            status='PA',
            is_last=True,
        )
        Payment.objects.create(
            user=self.test_user4,
            period_start=date,
            period_end=date,
            pay_date=date,
            basic_salary=self.test_user4.salary,
            total_payments=self.test_user4.salary,
            np_leave=0,
            total_deductions=self.test_user4.salary - 1500,
            mpf_employer=1500,
            mpf_employee=1500,
            net_pay=self.test_user4.salary - 1500,
            status='PA',
            is_last=True,
        )

    ### LastPaymentCreateViewTest ###
    def test_redirects_if_not_logged_in_LastPaymentCreateViewTest(self):
        response = self.client.get(reverse_lazy('payroll:create_last_payment'))
        self.assertRedirects(response, '/login/?next=/payroll/last/create/')

    def test_forbidden_if_not_superuser_LastPaymentCreateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/create/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LastPaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/create/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LastPaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy('payroll:create_last_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    def test_redirects_if_create_payment_success_LastPaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-10-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('payroll:create_last_payment'),
            {
                'user': self.test_user2.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
                'unused_leave_days': 0.0,
                'unused_leave_pay': 0.00,
                'date_joined': self.test_user2.date_joined,
                'is_last': True,
            })
        self.assertRedirects(response, reverse_lazy('payroll:index'))
        obj_exists = True if Payment.objects.get(
            user=self.test_user2, period_start=date) else False
        self.assertTrue(obj_exists)

    def test_create_payment_fail_overlapping_date_LastPaymentCreateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        response = self.client.post(
            reverse_lazy('payroll:create_payment'),
            data={
                'user': self.test_user2.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
                'unused_leave_days': 0.0,
                'unused_leave_pay': 0.00,
                'date_joined': self.test_user2.date_joined,
                'is_last': True,
            })
        self.assertEqual(response.status_code, 200)
        payment = Payment.objects.filter(user=self.test_user2,
                                         period_start__lte=date,
                                         period_end__gte=date
                                         ).exclude(status="CC").first()
        msg = f'Payment overlapping with {payment}'
        self.assertFormError(response, 'form', None, msg)

    ### LastPaymentUpdateViewTest ###
    def test_redirects_if_not_logged_in_LastPaymentUpdateViewTest(self):
        response = self.client.get('/payroll/last/update/1/')
        self.assertRedirects(response, '/login/?next=/payroll/last/update/1/')

    def test_forbidden_if_not_superuser_LastPaymentUpdateViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/update/2/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LastPaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/update/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LastPaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:update_last_payment', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    def test_redirects_after_update_payment_success_LastPaymentUpdateViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d').date()
        status = Payment.objects.get(id=4).status
        response = self.client.post(
            '/payroll/update/4/',
            data={
                'user': self.test_user4.id,
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': self.test_user2.salary,
                'total_payments': self.test_user2.salary,
                'np_leave': 0,
                'total_deductions': self.test_user2.salary - 1500,
                'mpf_employer': 1500,
                'mpf_employee': 1500,
                'net_pay': self.test_user2.salary - 1500,
                'method': 'CA',
                'status': 'PA',
                'cancel': 'cancel',
                'unused_leave_days': 0.0,
                'unused_leave_pay': 0.00,
                'date_joined': self.test_user2.date_joined,
                'is_last': True,
            })
        self.assertRedirects(response, reverse_lazy('payroll:index'))
        status = Payment.objects.get(id=4).status
        self.assertEquals(status, 'CC')

    ### LastPaymentDetailViewTest ###
    def test_redirects_if_not_logged_in_LastPaymentDetailViewTest(self):
        response = self.client.get('/payroll/last/detail/2/')
        self.assertRedirects(
            response, '/login/?next=/payroll/last/detail/2/')

    def test_forbidden_if_not_superuser_LastPaymentDetailViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/detail/1/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LastPaymentDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/detail/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LastPaymentDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:detail_last_payment', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_payment.html')

    def test_get_context_data_LastPaymentDetailViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:detail_last_payment', kwargs={'pk': 4}))
        self.assertEqual(
            response.context['date_joined'], self.test_user4.date_joined)

    ### LastPaymentPDFViewTest ###
    def test_redirects_if_not_logged_in_LastPaymentPDFViewTest(self):
        response = self.client.get('/payroll/last/payslipPDF/2/')
        self.assertRedirects(
            response, '/login/?next=/payroll/last/payslipPDF/2/')

    def test_forbidden_if_not_superuser_and_owner_LastPaymentPDFViewTest(self):
        self.client.login(username='testuser2', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/payslipPDF/4/')
        self.assertEqual(response.status_code, 403)

    def test_logged_in_url_exists_at_desired_location_LastPaymentPDFViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/payroll/last/payslipPDF/2/')
        self.assertEqual(response.status_code, 200)

    def test_logged_in_url_accessible_by_name_and_uses_correct_template_LastPaymentPDFViewTest(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse_lazy(
            'payroll:last_payslip_pdf', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payslip_pdf.html')
