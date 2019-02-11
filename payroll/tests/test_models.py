from django.test import TestCase
from personal_details.models import User
from payroll.models import Payment

import datetime
# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '234561'
salary = 20000
string = 'Testing'
date = datetime.datetime.strptime('2019-1-1', '%Y-%m-%d').date()
date_two = datetime.datetime.strptime('2019-4-24', '%Y-%m-%d').date()
date_three = datetime.datetime.strptime('2019-6-24', '%Y-%m-%d').date()
date_joined = datetime.datetime.strptime('2019-2-1-+0800', '%Y-%m-%d-%z')


class PayrollModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
            username=staff_id,
            password=staff_id,
            date_joined=date_joined,
        )
        # user join == period_start
        Payment.objects.create(
            user=cls.user,
            period_start=date,
            period_end=date,
            pay_date=date,
            basic_salary=salary,
            total_payments=salary,
            np_leave=0,
            total_deductions=salary * 0.05,
            mpf_employer=salary * 0.05,
            mpf_employee=salary * 0.05,
            net_pay=salary * 0.95,
        )
        # user joined 3 months
        Payment.objects.create(
            user=cls.user,
            period_start=date_two,
            period_end=date_two,
            pay_date=date_two,
            basic_salary=salary,
            total_payments=salary,
            np_leave=0,
            total_deductions=salary * 0.05,
            mpf_employer=salary * 0.05,
            mpf_employee=salary * 0.05,
            net_pay=salary * 0.95,
        )
        # user joined >3 months
        Payment.objects.create(
            user=cls.user,
            period_start=date_three,
            period_end=date_three,
            pay_date=date_three,
            basic_salary=salary,
            total_payments=salary,
            np_leave=0,
            total_deductions=salary * 0.05,
            mpf_employer=salary * 0.05,
            mpf_employee=salary * 0.05,
            net_pay=salary * 0.95,
        )

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    def test_payment_str(self):
        obj = Payment.objects.get(user=self.user, period_start=date)
        expected_result = f'{obj.user}: {obj.period_start} to {obj.period_end} of ${obj.net_pay}'
        self.assertEquals(str(obj), expected_result)

    def test_third_month_True(self):
        obj = Payment.objects.get(user=self.user, period_start=date_two)
        self.assertTrue(obj.third_month)

    def test_third_month_False_less_than_60(self):
        obj = Payment.objects.get(user=self.user, period_start=date)
        self.assertFalse(obj.third_month)

    def test_third_month_False_more_than_90(self):
        obj = Payment.objects.get(user=self.user, period_start=date_three)
        self.assertFalse(obj.third_month)

    def test_start_late_True(self):
        obj = Payment.objects.get(user=self.user, period_start=date)
        self.assertTrue(obj.start_late)

    def test_start_late_False(self):
        obj = Payment.objects.get(user=self.user, period_start=date_two)
        self.assertFalse(obj.start_late)
