from django.forms import ModelForm, ValidationError, DateInput, TextInput, PasswordInput, NumberInput, HiddenInput, CharField, ChoiceField, Select
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import hashers
from . import choices
from django.forms.models import inlineformset_factory

# Models
from .models import User, EmploymentHistory, Spouse, AcademicRecord, SalaryTitleRecord
from django.template.defaultfilters import slugify

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText
from swhr.utils import Formset

import datetime


class UserForm(ModelForm):
    spouse_name = CharField(label='Spouse Name', required=False)
    spouse_identity_type = ChoiceField(
        label='Spouse Identity Type', choices=choices.IDENTITY_TYPE, required=False)
    spouse_identity_no = CharField(label='Spouse Identity No.', required=False)

    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser',
                   'is_staff', 'groups', 'user_permissions']
        labels = {
            'first_name': "First Name",
            'last_name': "Last Name",
            'date_joined': "Date Joined",
        }
        help_texts = {
            'username': '',
            'is_active': '',
        }
        widgets = {
            'date_joined': DateInput(),
            'annual_leave': NumberInput(attrs={'class': 'one-decimal'}),
            'username': HiddenInput(),
            'password': HiddenInput(),
            'birth_date': DateInput(),
            'salary': NumberInput(attrs={'class': 'two-decimal'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
                <div class="border container col-sm-12">
                    <label class="col-form-label font-weight-bold text-info">Basic Info</label>
            '''),
            'username',
            'password',
            Row(
                Column(Field('staff_id', readonly=True),
                       css_class='col-sm-3'),
                Column('last_name', css_class='col-md-3'),
                Column('first_name', css_class='col-md-3'),
                Column('nick_name', css_class='col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column('mobile', css_class='col-sm-2'),
                Column('email', css_class='col-sm-3'),
                Column('birth_date', css_class='col-md-2'),
                Column('identity_type', css_class='col-md-2'),
                Column('identity_no', css_class='col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column('department', css_class='col-sm-3'),
                Column('title', css_class='col-sm-3'),
                Column(PrependedText('salary', '$'),
                       css_class='col-md-2'),
                Column('grade', css_class='col-sm-2'),
                Column(AppendedText('annual_leave', 'Days'),
                       css_class='col-md-2'),
                css_class='form-row'
            ),
            Row(
                Column('bank', css_class='col-md-5'),
                Column('bank_acc', css_class='col-md-2'),
                Column('date_joined', css_class='col-md-2'),
                Column('last_date', css_class='col-md-2'),
                Column(PrependedText('is_active', ''),
                       css_class='col-md-1'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='col-sm-12'),
                css_class='form-row'
            ),
            Row(
                Column('marital_status', css_class='col-sm-2'),
                Column('spouse_name', css_class='col-sm-3'),
                Column('spouse_identity_type', css_class='col-sm-2'),
                Column('spouse_identity_no', css_class='col-sm-3'),
                css_class='form-row'
            ),
            Row(
                Column('emergency_contact_name', css_class='col-md-3'),
                Column('emergency_contact_number', css_class='col-md-3'),
                Column('emergency_contact_relationship', css_class='col-md-3'),
                css_class='form-row'
            ),
            HTML('''
                </div>
                <div class="container col-sm-12 border">
                    <label class="col-form-label font-weight-bold text-primary">Academic Record</label>
                    <!--
                    <table style="width:100%;" class="academic-record-formset">
                        <thead>
                        <tr>
                            <th class="pr-2">Start Date</th>
                            <th class="pr-2">End Date</th>
                            <th class="pr-2">Institution Name</th>
                            <th class="pr-2">Qualification</th>
                            <th class="pr-2">Year</th>
                            <th></th>
                        </tr>
                        </thead>
                        <tbody>-->
            '''),
            Formset('ARFormset', 'ARFormsetHelper'),
            HTML('''
                    </tbody>
                </table>
                </div>
                <div class="container col-sm-12 border">
                    <label class="col-form-label font-weight-bold text-secondary">Employment History</label>'''),
            Formset('EHFormset', 'EHFormsetHelper'),
            HTML('''
                </div>
            '''),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'personal_details:index\' %}" class="btn btn-outline-secondary mt-2 mb-2" role="button">Back</a>')
        )

        # Required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['first_name'].initial = 'User'
        self.fields['last_name'].initial = 'Test'
        self.fields['date_joined'].initial = datetime.date.today()
        self.fields['birth_date'].initial = datetime.date.today()

    def clean(self):
        data = super().clean()
        if data['marital_status'] != 'SI' and not (data['spouse_name'] or data['spouse_identity_no']):
            msg = 'This field is required if user is not single.'
            self.add_error('spouse_name', msg)
            self.add_error('spouse_identity_no', msg)
        return super().clean()


class UserCreateForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['last_date'].disabled = True
        self.fields['is_active'].disabled = True

    def clean(self):
        data = super().clean()
        data['slug'] = slugify(data['staff_id'])
        data['username'] = data['staff_id']
        data['password'] = hashers.make_password(data['staff_id'].strip())
        return data


class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")
        self.helper.layout.insert(-2,
                                  HTML('''<div class="container col-sm-12 border">
                                            <label class="col-form-label font-weight-bold text-warning">Salary & Title</label>
                                            <table style="width:100%; class="table">
                                                <thead>
                                                <tr>
                                                    <th class="pr-2" style="width:8%;">Date</th>
                                                    <th class="pr-2" style="width:25%;">Department</th>
                                                    <th class="pr-2" style="width:25%;">Title</th>
                                                    <th class="pr-2" style="width:16.6667%;">Salary</th>
                                                    <th class="pr-2" style="width:8%;">Grade</th>
                                                </tr>
                                                </thead>
                                                <tbody>
                                  '''))
        self.helper.layout.insert(-2, Formset('STFormset', 'STFormsetHelper'))
        self.helper.layout.insert(-2,  HTML('''</tbody></table></div>'''))

        # Should not be able to update any of these
        for name in ['username', 'password', 'staff_id', 'slug']:
            self.fields[name].disabled = True

        if not self.user.is_superuser:
            self.helper.layout.insert(-1, HTML(
                '<a href="{% url \'change_password\' %}" class="btn btn-outline-info" role="button">Change Password</a> '))
            self.helper.layout.pop(-1)

            for name in ['nick_name', 'bank', 'bank_acc', 'mobile',
                         'email', 'address', 'emergency_contact_name',
                         'emergency_contact_number', 'emergency_contact_relationship']:
                self.fields[name].disabled = True

            self.fields['last_date'].widget = HiddenInput()
            self.fields['is_active'].widget = HiddenInput()
        else:
            self.fields['date_joined'].disabled = True

    def clean(self):
        data = super().clean()
        if not data['is_active'] and not data['last_date']:
            self.add_error(
                last_date, 'This field is required if staff is inactive.')
        return super().clean()


class AcademicRecordForm(ModelForm):
    class Meta:
        model = AcademicRecord
        fields = '__all__'

    def clean_year_completed(self):
        year_completed = self.cleaned_data['year_completed']
        if year_completed != '' and int(year_completed) > datetime.date.today().year:
            raise ValidationError(
                'Completed year is larger than current year.')
        return year_completed


class AcademicRecordFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AcademicRecordFormsetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Row(
                Column('date_start', css_class='col-sm-1'),
                Column('date_end', css_class='col-sm-1'),
                Column('institution_name', css_class='col-sm-4'),
                Column('qualification', css_class='col-sm-4'),
                Column('year_completed', css_class='col-sm-1'),
                Column(
                    HTML('''<a role="button" class="fas fa-minus-circle text-danger minus-ar-btn" style="font-size:1.5rem; padding-top:45px;"></a>'''),
                    css_class='col-sm-1 text-center'),
                'user',
                'id',
                Column('DELETE', css_class='d-none'),
                css_class='form-row academic-record-formset'
            ),
        )


class EmploymentHistoryForm(ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = '__all__'


class EmploymentHistoryFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EmploymentHistoryFormsetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            # HTML('''<tr><td class="pr-2">'''),
            # 'date_start',
            # HTML('''</td><td class="pr-2">'''),
            # 'date_end',
            # HTML('''</td><td class="pr-2">'''),
            # 'employer_name',
            # HTML('''</td><td class="pr-2">'''),
            # 'position',
            # HTML('''</td><td class="pr-2">'''),
            # 'reason',
            # HTML('''</td><td class="pr-2">'''),
            # HTML('''<a role="button" class="fas fa-minus-circle text-danger minus-eh-btn" style="font-size:1.5rem; padding-top:45px;"></a>'''),
            # 'user',
            # 'id',
            # Field('DELETE', css_class='d-none'),
            # HTML('''</td></tr>'''),
            Row(
                Column('date_start', css_class='col-sm-1'),
                Column('date_end', css_class='col-sm-1'),
                Column('employer_name', css_class='col-sm-3'),
                Column('position', css_class='col-sm-2'),
                Column('reason', css_class='col-md-4'),
                Column(HTML('''<a role="button" class="fas fa-minus-circle text-danger minus-eh-btn" style="font-size:1.5rem; padding-top:45px;"></a>'''),
                       css_class='col-md-1 text-center'),
                'user',
                'id',
                Column('DELETE', css_class='d-none'),
                css_class='form-row employment-history-formset'
            ),
        )


class SalaryTitleRecordForm(ModelForm):
    class Meta:
        model = SalaryTitleRecord
        fields = '__all__'
        widgets = {
            'date_changed': DateInput(),
            'salary': NumberInput(attrs={'class': 'two-decimal'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalaryTitleRecordForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.disabled = True


class SalaryTitleRecordFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SalaryTitleRecordFormsetHelper, self).__init__(*args, **kwargs)
        self.form_show_labels = False
        self.layout = Layout(
            HTML('''<tr><td class="pr-2">'''),
            'date_changed',
            HTML('''</td><td class="pr-2">'''),
            'department',
            HTML('''</td><td class="pr-2">'''),
            'title',
            HTML('''</td><td class="pr-2">'''),
            'salary',
            HTML('''</td><td class="pr-2">'''),
            'grade',
            HTML('''</td></tr>'''),
            # Row(
            #     Column('date_changed', css_class='col-sm-1'),
            #     Column('department', css_class='col-sm-3'),
            #     Column('title', css_class='col-sm-3'),
            #     Column('salary', css_class='col-sm-2'),
            #     Column('grade', css_class='col-md-2'),
            #     css_class='form-row salary-title-formset'
            # ),
        )
