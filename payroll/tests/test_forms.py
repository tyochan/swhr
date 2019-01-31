from django.test import TestCase
from personal_details.models import User
from payroll.models import Payment
from payroll.forms import PaymentForm, PaymentCreateForm, PaymentDetailForm, PaymentUpdateForm, LastPaymentForm, LastPaymentCreateForm, LastPaymentUpdateForm, LastPaymentDetailForm

import datetime
import calendar

# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '234561'
staff_id_two = '456789'
date = datetime.datetime.strptime('2019-1-3', '%Y-%m-%d')
date_two = datetime.datetime.strptime('2019-3-3', '%Y-%m-%d')
salary = 20000


class PayrollFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            first_name=first_name, last_name=last_name,
            staff_id=staff_id, slug=staff_id,
            username=staff_id, password=staff_id,
            annual_leave=15,
        )
        cls.superuser = User.objects.create(
            first_name=first_name, last_name=last_name,
            staff_id=staff_id_two, slug=staff_id,
            username=staff_id_two, password=staff_id_two,
            is_superuser=True,
        )
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

    def test_payment_form(self):
        form = PaymentForm()
        self.assertEquals(
            type(form.fields['user'].widget).__name__, 'Select'
        )

        date = datetime.date.today()
        period_start = date.replace(day=1)
        period_end = date.replace(day=calendar.monthrange(
            period_start.year, period_start.month)[1])
        self.assertEquals(
            form.fields['period_start'].initial, period_start
        )
        self.assertEquals(
            form.fields['period_end'].initial, period_end
        )
        self.assertEquals(
            form.fields['pay_date'].initial, date
        )
        self.assertTrue(
            form.fields['status'].disabled
        )

    def test_payment_create_with_valid_data(self):
        form = PaymentCreateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date_two,
                'period_end': date_two,
                'pay_date': date_two,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        self.assertTrue(form.is_valid())

    def test_payment_create_with_overlapped_date(self):
        form = PaymentCreateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        self.assertFalse(form.is_valid())

    def test_payment_update_form(self):  # Superuser only
        form = PaymentUpdateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )

        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

        save_btn, cancel_btn, export_btn = False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'html'):
                if 'id="id_export_pdf"' in obj.html:
                    export_btn = True
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                if 'cancel' in obj.name:
                    cancel_btn = True

        self.assertFalse(save_btn)
        self.assertTrue(cancel_btn)
        self.assertTrue(export_btn)

    def test_payment_detail_form_for_normal_user(self):
        form = PaymentDetailForm(
            user=self.user,
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        save_btn, cancel_btn, export_btn = False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'html'):
                if 'id="id_export_pdf"' in obj.html:
                    export_btn = True
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                if 'cancel' in obj.name:
                    cancel_btn = True

        self.assertFalse(save_btn)
        self.assertFalse(cancel_btn)
        self.assertTrue(export_btn)

        self.assertEquals(form.user, self.user)
        self.assertEquals(form.fields['user'].initial, self.user.id)
        self.assertTrue(form.fields['user'].disabled)

    def test_last_payment_form(self):
        form = LastPaymentForm()
        self.assertEquals(
            type(form.fields['period_end'].widget).__name__, 'DateInput'
        )
        self.assertEquals(
            type(
                form.fields['unused_leave_days'].widget).__name__, 'NumberInput'
        )
        self.assertEquals(
            type(
                form.fields['unused_leave_pay'].widget).__name__, 'NumberInput'
        )
        self.assertEquals(
            type(
                form.fields['date_joined'].widget).__name__, 'DateInput'
        )
        self.assertTrue(
            'one-decimal' in form.fields['unused_leave_days'].widget.attrs['class'])
        self.assertTrue(
            'two-decimal' in form.fields['unused_leave_pay'].widget.attrs['class'])
        self.assertTrue(form.fields['is_last'].initial)

    def test_last_payment_create_form_valid_data(self):
        form = LastPaymentCreateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date_two,
                'period_end': date_two,
                'pay_date': date_two,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        self.assertTrue(form.is_valid())

    def test_last_payment_create_form_overlapping_payment(self):
        form = LastPaymentCreateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date,
                'period_end': date,
                'pay_date': date,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        self.assertFalse(form.is_valid())

    def test_last_payment_update_form(self):
        form = LastPaymentUpdateForm(
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date_two,
                'period_end': date_two,
                'pay_date': date_two,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        save_btn, cancel_btn, export_btn = False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'html'):
                if 'id="id_export_pdf"' in obj.html:
                    export_btn = True
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                if 'cancel' in obj.name:
                    cancel_btn = True

        self.assertFalse(save_btn)
        self.assertTrue(cancel_btn)
        self.assertTrue(export_btn)

        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

    def test_last_payment_detail_form_for_normal_user(self):
        form = LastPaymentDetailForm(
            user=self.user,
            data={
                'user': self.user.id,
                'method': 'TR',
                'period_start': date_two,
                'period_end': date_two,
                'pay_date': date_two,
                'basic_salary': salary,
                'total_payments': salary,
                'np_leave': 0,
                'total_deductions': salary * 0.05,
                'mpf_employer': salary * 0.05,
                'mpf_employee': salary * 0.05,
                'net_pay': salary * 0.95,
            }
        )
        save_btn, cancel_btn, export_btn = False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'html'):
                if 'id="id_export_pdf"' in obj.html:
                    export_btn = True
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                if 'cancel' in obj.name:
                    cancel_btn = True

        self.assertFalse(save_btn)
        self.assertFalse(cancel_btn)
        self.assertTrue(export_btn)

        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

        self.assertEquals(form.user, self.user)
        self.assertEquals(form.fields['user'].initial, self.user.id)
        self.assertTrue(form.fields['user'].disabled)
