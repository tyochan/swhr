from django.test import TestCase
from django.urls import reverse_lazy

from personal_details.models import User
from leave_records.models import Leave
from payroll.models import Payment
from payroll import choices
from payroll import views

import datetime

max_mpf = 1500
s1, s2, s3 = 7000, 18550, 35000


class PayrollViewUtilsTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.period_min = datetime.datetime.strptime(
            '2019-4-2', '%Y-%m-%d').date()
        self.period_max = datetime.datetime.strptime(
            '2019-4-5', '%Y-%m-%d').date()
        self.period_start = datetime.datetime.strptime(
            '2018-1-24', '%Y-%m-%d').date()

        # Create two users
        self.test_user1 = User.objects.create_superuser(
            username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com', salary=50000)
        self.test_user2 = User.objects.create_user(
            username='testuser2', password='1X<ISRUkw+tuK', salary=s1)
        self.test_user3 = User.objects.create_user(
            username='testuser3', password='1X<ISRUkw+tuK', salary=s2)
        self.test_user4 = User.objects.create_user(
            username='testuser4', password='1X<ISRUkw+tuK', salary=s3)

        self.test_user1.save()
        self.test_user2.save()
        self.test_user3.save()
        self.test_user4.save()

        date = self.period_start
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
                mpf_employer=0,
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
                mpf_employer=0,
                mpf_employee=0,
                net_pay=self.test_user3.salary,
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
                mpf_employer=0,
                mpf_employee=0,
                net_pay=self.test_user4.salary,
                status='PA',
            )
            date = date.replace(month=date.month + 1)

    def test_limit_period_start_before_period(self):
        date = datetime.datetime.strptime('2019-4-1', '%Y-%m-%d').date()
        start_date, end_date = views.limit_period(
            date, date, self.period_min, self.period_max)
        self.assertEqual(start_date, self.period_min)
        self.assertEqual(end_date, date)

    def test_limit_period_end_after_period(self):
        date = datetime.datetime.strptime('2019-4-6', '%Y-%m-%d').date()
        start_date, end_date = views.limit_period(
            date, date, self.period_min, self.period_max)
        self.assertEqual(start_date, date)
        self.assertEqual(end_date, self.period_max)

    def test_get_mpf_salary_less_than_7100_and_passed_less_than_60_days(self):
        user = User.objects.get(id=2)
        period_start = self.period_start + datetime.timedelta(days=50)
        mpf_employer, mpf_employee = views.get_mpf(
            s1, 50, user, period_start)
        self.assertEqual(mpf_employer, 0)
        self.assertEqual(mpf_employee, 0)

    def test_get_mpf_salary_within_7100_to_30000_and_passed_less_than_60_days(self):
        user = User.objects.get(id=3)
        period_start = self.period_start + datetime.timedelta(days=50)
        mpf_employer, mpf_employee = views.get_mpf(
            s2, 50, user, period_start)
        self.assertEqual(mpf_employer, 0)
        self.assertEqual(mpf_employee, 0)

    def test_get_mpf_salary_more_than_30000_and_passed_less_than_60_days(self):
        user = User.objects.get(id=4)
        period_start = self.period_start + datetime.timedelta(days=50)
        mpf_employer, mpf_employee = views.get_mpf(
            s3, 50, user, period_start)
        self.assertEqual(mpf_employer, 0)
        self.assertEqual(mpf_employee, 0)

    def test_get_mpf_salary_less_than_7100_for_third_month(self):
        user = User.objects.get(id=2)
        period_start = self.period_start + datetime.timedelta(days=80)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 80, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        expected_mpf_employer = 0
        for p in payments:
            expected_mpf_employer += p.net_pay * 0.05
        expected_mpf_employer += user.salary * 0.05
        self.assertEqual(mpf_employer, expected_mpf_employer)
        self.assertEqual(mpf_employee, 0)

    def test_get_mpf_salary_within_7100_to_30000_for_third_month(self):
        user = User.objects.get(id=3)
        period_start = self.period_start + datetime.timedelta(days=80)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 80, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        expected_mpf_employer = 0
        for p in payments:
            expected_mpf_employer += p.net_pay * 0.05
        expected_mpf_employer += user.salary * 0.05
        self.assertEqual(mpf_employer, expected_mpf_employer)
        self.assertEqual(mpf_employee, user.salary * 0.05)

    def test_get_mpf_salary_more_than_30000_for_third_month(self):
        user = User.objects.get(id=4)
        period_start = self.period_start + datetime.timedelta(days=80)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 80, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        expected_mpf_employer = 0
        for p in payments:
            expected_mpf_employer += max_mpf
        expected_mpf_employer += max_mpf
        self.assertEqual(mpf_employer, expected_mpf_employer)
        self.assertEqual(mpf_employee, max_mpf)

    def test_get_mpf_salary_less_than_7100_for_more_than_third_month(self):
        user = User.objects.get(id=2)
        period_start = self.period_start + datetime.timedelta(days=90)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 90, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        self.assertEqual(mpf_employer, user.salary * 0.05)
        self.assertEqual(mpf_employee, 0)

    def test_get_mpf_salary_within_7100_to_30000_for_more_than_third_month(self):
        user = User.objects.get(id=3)
        period_start = self.period_start + datetime.timedelta(days=90)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 90, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        self.assertEqual(mpf_employer, user.salary * 0.05)
        self.assertEqual(mpf_employee, user.salary * 0.05)

    def test_get_mpf_salary_more_than_30000_for_more_than_third_month(self):
        user = User.objects.get(id=4)
        period_start = self.period_start + datetime.timedelta(days=90)
        mpf_employer, mpf_employee = views.get_mpf(
            user.salary, 90, user, period_start)
        payments = Payment.objects.filter(
            user=user, period_end__lte=period_start)
        self.assertEqual(mpf_employer, max_mpf)
        self.assertEqual(mpf_employee, max_mpf)
