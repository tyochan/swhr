from django.test import TestCase
from personal_details.models import User, AcademicRecord, EmploymentHistory, SalaryTitleRecord, Spouse

# Create your tests here.
first_name = 'First'
last_name = 'Last'
staff_id = '123456'
username = '123456'
password = '123456'
date = '2019-1-1'
salary = 20000
string = 'Testing'


class ProfileModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            staff_id=staff_id,
            username=username,
            password=password,
        )
        AcademicRecord.objects.create(
            user=user,
            date_start=date,
            date_end=date,
            institution_name=string,
            qualification=string,
        )
        EmploymentHistory.objects.create(
            user=user,
            date_start=date,
            date_end=date,
            employer_name=string,
            position=string,
            reason=string,
        )
        SalaryTitleRecord.objects.create(
            user=user,
            date_changed=date,
            salary=user.salary,
            title=string,
        )
        Spouse.objects.create(
            user=user,
            name=string,
            identity_no=string,
        )

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    def test_user_get_absolute_url(self):
        obj = User.objects.get(staff_id=staff_id)
        self.assertEquals(obj.get_absolute_url(), '/personal_details/')

    def test_user_str(self):
        obj = User.objects.get(staff_id=staff_id)
        expected_result = f'{obj.staff_id} {obj.last_name} {obj.first_name}'
        self.assertEquals(str(obj), expected_result)

    def test_user_get_name(self):
        obj = User.objects.get(staff_id=staff_id)
        expected_result = f'{obj.last_name} {obj.first_name}'
        self.assertEquals(obj.get_name(), expected_result)

    def test_AcademicRecord_str(self):
        user = User.objects.get(staff_id=staff_id)
        obj = AcademicRecord.objects.get(user=user)
        expected_result = f'{obj.date_start} {obj.date_end} {obj.institution_name} {obj.qualification} {obj.year_completed}'
        self.assertEquals(str(obj), expected_result)

    def test_EmploymentHistory_str(self):
        user = User.objects.get(staff_id=staff_id)
        obj = EmploymentHistory.objects.get(user=user)
        expected_result = f'{obj.date_start} to {obj.date_end} {obj.employer_name} {obj.position} {obj.reason}'
        self.assertEquals(str(obj), expected_result)

    def test_SalaryTitleRecord_str(self):
        user = User.objects.get(staff_id=staff_id)
        obj = SalaryTitleRecord.objects.get(user=user)
        expected_result = f'{obj.date_changed} {obj.title} {obj.grade} {obj.salary}'
        self.assertEquals(str(obj), expected_result)

    def test_Spouse_str(self):
        user = User.objects.get(staff_id=staff_id)
        obj = Spouse.objects.get(user=user)
        expected_result = f'{obj.user} {obj.name} {obj.identity_type} {obj.identity_no}'
        self.assertEquals(str(obj), expected_result)

    # def test_login(self):
    #     user = User.objects.get(staff_id=staff_id)

    # def test_nick_name_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('nick_name').verbose_name
    #     self.assertEquals(field_label, 'Nick Name')
    #
    # def test_staff_id_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('staff_id').verbose_name
    #     self.assertEquals(field_label, 'Employee ID')
    #
    # def test_birth_date_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('birth_date').verbose_name
    #     self.assertEquals(field_label, 'Date of Birth')
    #
    # def test_identity_type_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('identity_type').verbose_name
    #     self.assertEquals(field_label, 'Identity Type')
    #
    # def test_identity_no_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('identity_no').verbose_name
    #     self.assertEquals(field_label, 'Identity No')
    #
    # def test_mobile_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('mobile').verbose_name
    #     self.assertEquals(field_label, 'mobile')
    #
    # def test_address_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('address').verbose_name
    #     self.assertEquals(field_label, 'address')
    #
    # def test_department_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('department').verbose_name
    #     self.assertEquals(field_label, 'department')
    #
    # def test_title_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('title').verbose_name
    #     self.assertEquals(field_label, 'title')
    #
    # def test_grade_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('grade').verbose_name
    #     self.assertEquals(field_label, 'grade')
    #
    # def test_marital_status_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('marital_status').verbose_name
    #     self.assertEquals(field_label, 'Marital Status')
    #
    # def test_old_annual_leave_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('old_annual_leave').verbose_name
    #     self.assertEquals(field_label, 'Old Annual Leave')
    #
    # def test_annual_leave_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('annual_leave').verbose_name
    #     self.assertEquals(field_label, 'Annual Leave')
    #
    # def test_bank_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('bank').verbose_name
    #     self.assertEquals(field_label, 'bank')
    #
    # def test_bank_acc_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('bank_acc').verbose_name
    #     self.assertEquals(field_label, 'Bank Account')
    #
    # def test_salary_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('salary').verbose_name
    #     self.assertEquals(field_label, 'salary')
    #
    # def test_emergency_contact_name_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field(
    #         'emergency_contact_name').verbose_name
    #     self.assertEquals(field_label, 'Emergency Contact Person')
    #
    # def test_emergency_contact_number_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field(
    #         'emergency_contact_number').verbose_name
    #     self.assertEquals(field_label, 'Emergency Contact Number')
    #
    # def test_emergency_contact_relationship_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field(
    #         'emergency_contact_relationship').verbose_name
    #     self.assertEquals(field_label, 'Relationship')
    #
    # def test_last_date_label(self):
    #     obj = User.objects.get(staff_id=staff_id)
    #     field_label = obj._meta.get_field('last_date').verbose_name
    #     self.assertEquals(field_label, 'Last Date')
