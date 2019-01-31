from django.test import TestCase
from leave_records.forms import LeaveForm, LeaveCreateForm, LeaveDetailForm, LeaveUpdateForm
from personal_details.models import User
from leave_records.models import Leave

import datetime

# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '234561'
staff_id_two = '456789'
date = datetime.datetime.strptime('2019-1-3', '%Y-%m-%d')
salary = 20000
string = 'Testing'
date_start = datetime.datetime.strptime('2019-1-2', '%Y-%m-%d')
date_start_a = datetime.datetime.strptime('2019-1-4', '%Y-%m-%d')
date_end = datetime.datetime.strptime('2019-1-5', '%Y-%m-%d')


class LeaveFormTest(TestCase):
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
        Leave.objects.create(
            user=cls.user,
            start_date=date,
            end_date=date,
            spend=0,
            type='AL',
            day_type='HD',
            remarks='',
        )

    def test_leave_form(self):
        form = LeaveForm(user=self.user)
        self.assertEquals(
            type(form.fields['remarks'].widget).__name__, 'Textarea'
        )
        self.assertEquals(
            type(form.fields['spend'].widget).__name__, 'NumberInput'
        )
        self.assertTrue(
            'one-decimal' in form.fields['spend'].widget.attrs['class']
        )
        self.assertTrue(
            form.fields['status'].disabled
        )

    def test_leave_create_form_for_normal_user(self):
        form = LeaveCreateForm(user=self.user)
        self.assertEquals(form.user, self.user)
        self.assertEquals(
            type(form.fields['user'].widget).__name__, 'Select'
        )
        self.assertEquals(
            form.fields['user'].label, 'Employee'
        )
        self.assertEquals(
            form.fields['user'].initial, self.user.id
        )
        self.assertTrue(
            form.fields['user'].disabled
        )

    def test_leave_create_form_for_super_user(self):
        form = LeaveCreateForm(user=self.superuser)
        self.assertEquals(form.user, self.superuser)
        self.assertEquals(
            type(form.fields['user'].widget).__name__, 'Select'
        )
        self.assertFalse(
            form.fields['user'].disabled
        )

    def test_leave_create_form_valid_half_day(self):
        form = LeaveCreateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date,
                'end_date': date,
                'spend': 0.5,
                'type': 'AL',
                'day_type': 'HD',
                'remarks': '',
            }
        )
        self.assertTrue(form.is_valid())

    def test_leave_create_form_spend_less_than_quota(self):
        form = LeaveCreateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date_start_a,
                'end_date': date_end,
                'spend': 2,
                'type': 'AL',
                'day_type': 'FD',
                'remarks': '',
            }
        )
        self.assertTrue(form.is_valid())

    def test_leave_create_form_invalid_half_day(self):
        Leave.objects.create(
            user=self.user,
            start_date=date,
            end_date=date,
            spend=0,
            type='AL',
            day_type='HD',
            remarks='',
        )
        form = LeaveCreateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date,
                'end_date': date,
                'spend': 0.5,
                'type': 'AL',
                'day_type': 'HD',
                'remarks': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_leave_create_form_spend_exceeds_quota(self):
        form = LeaveCreateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date_start_a,
                'end_date': date_end,
                'spend': 100,
                'type': 'AL',
                'day_type': 'FD',
                'remarks': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_leave_create_form_overlapping_leave(self):
        form = LeaveCreateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date_start,
                'end_date': date_end,
                'spend': 5,
                'type': 'AL',
                'day_type': 'FD',
                'remarks': '',
            }
        )
        self.assertFalse(form.is_valid())

    def test_leave_detail_form(self):
        form = LeaveDetailForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date_start,
                'end_date': date_end,
                'spend': 5,
                'type': 'AL',
                'day_type': 'FD',
                'remarks': '',
            }
        )
        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

        save_btn = False
        for obj in form.helper.layout:
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                    break
        self.assertFalse(save_btn)

    def test_leave_update_form(self):
        form = LeaveUpdateForm(
            user=self.superuser,
            data={
                'user': self.user.id,
                'start_date': date_start,
                'end_date': date_end,
                'spend': 5,
                'type': 'AL',
                'day_type': 'FD',
                'remarks': '',
            }
        )
        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

        save_btn, approve_btn, reject_btn = False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'name'):
                if 'save' in obj.name:
                    save_btn = True
                if 'approve' in obj.name:
                    approve_btn = True
                if 'reject' in obj.name:
                    reject_btn = True
        self.assertFalse(save_btn)
        self.assertTrue(approve_btn)
        self.assertTrue(reject_btn)
