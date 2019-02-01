from django.test import TestCase
from personal_details.models import User, AcademicRecord, EmploymentHistory, SalaryTitleRecord, Spouse
from personal_details.forms import UserForm, UserCreateForm, UserUpdateForm, AcademicRecordForm, AcademicRecordFormsetHelper, EmploymentHistoryForm, EmploymentHistoryFormsetHelper, SalaryTitleRecordForm, SalaryTitleRecordFormsetHelper

import datetime
# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '234561'
staff_id_two = '456789'
date = datetime.datetime.strptime('2019-1-3', '%Y-%m-%d')
date_two = datetime.datetime.strptime('2019-3-3', '%Y-%m-%d')
today = datetime.date.today()
salary = 20000


class UserFormTest(TestCase):
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

    def test_user_form(self):
        form = UserForm()
        self.assertEquals(
            type(form.helper).__name__, 'FormHelper')
        self.assertTrue(
            form.fields['first_name'].required)
        self.assertTrue(
            form.fields['last_name'].required)
        self.assertEquals(
            form.fields['date_joined'].initial, today)
        self.assertEquals(
            form.fields['birth_date'].initial, today)

    def test_user_form_valid_data_single_without_spouse(self):
        form = UserForm(
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertTrue(form.is_valid())

        save_btn, ARFormset, ARFormsetHelper, EHFormset, EHFormsetHelper = False, False, False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'formset_context_name'):
                if 'AR' in obj.formset_context_name:
                    ARFormset = True
                if 'AR' in obj.helper_context_name:
                    ARFormsetHelper = True
                if 'EH' in obj.formset_context_name:
                    EHFormset = True
                if 'EH' in obj.helper_context_name:
                    EHFormsetHelper = True
            if hasattr(obj, 'value'):
                if 'Save' in obj.value:
                    save_btn = True

        self.assertTrue(save_btn)
        self.assertTrue(ARFormset)
        self.assertTrue(ARFormsetHelper)
        self.assertTrue(EHFormset)
        self.assertTrue(EHFormsetHelper)

    def test_user_form_valid_data_married_with_spouse(self):
        form = UserForm(
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'MA',
                'spouse_name': first_name, 'spouse_identity_no': staff_id,
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_not_single_without_spouse(self):
        form = UserForm(
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'MA',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertFalse(form.is_valid())

    def test_user_create_form(self):
        form = UserCreateForm(
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertTrue(form.fields['last_date'].disabled)
        self.assertTrue(form.fields['is_active'].disabled)

    def test_user_update_form_for_normal_user(self):
        form = UserUpdateForm(
            user=self.user,
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertEquals(form.user, self.user)

        save_btn, update_btn, salary_title, change_password, bk_btn, STFormset, STFormsetHelper, = False, False, False, False, False, False, False
        for obj in form.helper.layout:
            if hasattr(obj, 'value'):
                if 'Save' in obj.value:
                    save_btn = True
                if 'Update' in obj.value:
                    update_btn = True
            if hasattr(obj, 'html'):
                if 'Salary & Title' in obj.html:
                    salary_title = True
                if 'change_password' in obj.html:
                    change_password = True
                if 'personal_details:index' in obj.html:
                    bk_btn = True
            if hasattr(obj, 'formset_context_name'):
                if 'ST' in obj.formset_context_name:
                    STFormset = True
                if 'ST' in obj.helper_context_name:
                    STFormsetHelper = True

        self.assertFalse(save_btn)
        self.assertTrue(update_btn)
        self.assertTrue(change_password)
        self.assertFalse(bk_btn)
        self.assertTrue(STFormset)
        self.assertTrue(STFormsetHelper)

        disabled = True
        for name, field in form.fields.items():
            if name not in ['nick_name', 'bank', 'bank_acc', 'mobile',
                            'email', 'address', 'emergency_contact_name',
                            'emergency_contact_number', 'emergency_contact_relationship'] and not field.disabled:
                disabled = False
        self.assertTrue(disabled)

        self.assertEquals(
            type(form.fields['last_date'].widget).__name__, 'HiddenInput')
        self.assertEquals(
            type(form.fields['is_active'].widget).__name__, 'HiddenInput')

    def test_user_update_form_for_super_user(self):
        form = UserUpdateForm(
            user=self.superuser,
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
            }
        )
        self.assertEquals(form.user, self.superuser)

        correctly_disabled = True
        for name, field in form.fields.items():
            if name not in ['username', 'password', 'staff_id', 'slug', 'date_joined'] and field.disabled:
                correctly_disabled = False
        self.assertTrue(correctly_disabled)

    def test_user_update_form_invalid_inactive_without_last_date(self):
        form = UserUpdateForm(
            user=self.superuser,
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
                'is_active': False,
            }
        )
        expected = True if 'last_date' in form.errors else False
        self.assertTrue(expected)
        self.assertFalse(form.is_valid())

    def test_user_update_form_valid_inactive_with_last_date(self):
        form = UserUpdateForm(
            user=self.superuser,
            data={
                'username': '87654321', 'password': '87654321',
                'staff_id': '87654321', 'first_name': first_name, 'last_name': last_name,
                'mobile': staff_id, 'email': 'test@81.com', 'birth_date': today,
                'identity_type': 'ID', 'identity_no': staff_id,
                'department': '63A', 'title': staff_id, 'salary': 0, 'grade': 'U1',
                'annual_leave': 15, 'bank': '003', 'bank_acc': staff_id,
                'date_joined': today, 'address': staff_id, 'marital_status': 'SI',
                'emergency_contact_name': staff_id, 'emergency_contact_number': staff_id,
                'emergency_contact_relationship': staff_id,
                'is_active': False, 'last_date': today,
            }
        )
        expected = True
        for obj in form.errors:
            if obj in ['username', 'password']:  # ignore as both are disabled in form
                continue
            expected = False
        self.assertTrue(expected)

    def test_academic_record_form_with_valid_data(self):
        form = AcademicRecordForm(
            data={
                'date_start': today, 'date_end': today,
                'institution_name': staff_id, 'qualification': staff_id,
                'year_completed': '2019', 'user': self.user.id
            }
        )
        self.assertTrue(form.is_valid())

    def test_academic_record_formset_helper(self):
        helper = AcademicRecordFormsetHelper()
        self.assertFalse(helper.form_show_labels)

    def test_employment_history_form_with_valid_data(self):
        form = EmploymentHistoryForm(
            data={
                'date_start': today, 'date_end': today,
                'employer_name': staff_id, 'position': staff_id,
                'reason': '2019', 'user': self.user.id
            }
        )
        self.assertTrue(form.is_valid())

    def test_employment_history_formset_helper(self):
        helper = EmploymentHistoryFormsetHelper()
        self.assertFalse(helper.form_show_labels)

    def test_salary_title_record_form_with_valid_data(self):
        form = SalaryTitleRecordForm(
            data={
                'date_changed': today, 'department': staff_id,
                'title': staff_id, 'salary': 20000,
                'grade': 'U1', 'user': self.user.id
            }
        )

        self.assertEquals(
            type(form.fields['date_changed'].widget).__name__, 'DateInput')
        self.assertEquals(
            type(form.fields['salary'].widget).__name__, 'NumberInput')
        self.assertTrue(
            'two-decimal' in form.fields['salary'].widget.attrs['class'])

        all_disabled = True
        for name, field in form.fields.items():
            if not field.disabled:
                all_disabled = False
        self.assertTrue(all_disabled)

    def test_salary_title_record_formset_helper(self):
        helper = SalaryTitleRecordFormsetHelper()
        self.assertFalse(helper.form_show_labels)
