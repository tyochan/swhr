from django.forms import ModelForm, ValidationError, DateInput, TextInput, PasswordInput, NumberInput, HiddenInput, CharField, ChoiceField, Select
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import hashers
from . import choices
from django.forms.models import inlineformset_factory

# Models
from .models import User, EmploymentHistory, Spouse, AcademicRecord

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
            Field('username', readonly=True),
            Field('password', readonly=True),
            Row(
                Column(Field('staff_id', readonly=True),
                       css_class='col-sm-3'),
                Column(Field('last_name'),
                       css_class='col-md-3'),
                Column(Field('first_name'),
                       css_class='col-md-3'),
                Column('nick_name', css_class='col-md-3'),

                css_class='form-row'
            ),
            Row(
                Column(Field('mobile'),
                       css_class='col-sm-2'),
                Column(Field('email'),
                       css_class='col-sm-3'),
                Column(Field('birth_date'),
                       css_class='col-md-2'),
                Column(Field('identity_type'),
                       css_class='col-md-2'),
                Column(Field('identity_no'),
                       css_class='col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('department'),
                       css_class='col-sm-3'),
                Column(Field('title'),
                       css_class='col-sm-3'),
                Column(PrependedText('salary', '$'),
                       css_class='col-md-2'),
                Column(Field('grade'),
                       css_class='col-sm-2'),
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
                Column(Field('address'),
                       css_class='col-sm-12'),
                css_class='form-row'
            ),
            Row(
                Column(Field('marital_status'),
                       css_class='col-sm-2'),
                Column(Field('spouse_name'),
                       css_class='col-sm-3'),
                Column(Field('spouse_identity_type'),
                       css_class='col-sm-2'),
                Column(Field('spouse_identity_no'),
                       css_class='col-sm-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('emergency_contact_name'),
                       css_class='col-md-3'),
                Column(Field('emergency_contact_number'),
                       css_class='col-md-3'),
                Column(Field('emergency_contact_relationship'),
                       css_class='col-md-3'),
                css_class='form-row'
            ),
            HTML('''
                </div>
                <div class="container col-sm-12 border">
                    <label class="col-form-label font-weight-bold text-primary">Academic Record</label>
            '''),
            Formset('ARFormset', 'ARFormsetHelper'),
            HTML('''
                </div>
                <div class="container col-sm-12 border">
                    <label class="col-form-label font-weight-bold text-secondary">Employment History</label>'''),
            Formset('EHFormset', 'EHFormsetHelper'),
            HTML('''
                </div>
            '''),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'personal_details:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>')
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
            raise ValidationError(
                'Spouse information is needed if user is not single.')
        return super().clean()


class UserCreateForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['last_date'].disabled = True
        self.fields['is_active'].disabled = True

    def clean_password(self):
        password = self.cleaned_data['password'].strip()
        password = hashers.make_password(password)
        return password


class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")

        if not self.user.is_superuser:
            self.helper.layout.insert(-1, HTML(
                '<a href="{% url \'change_password\' %}" class="btn btn-outline-info" role="button">Change Password</a> '))
            self.helper.layout.pop(-1)

            for name, field in self.fields.items():
                if name not in ['nick_name', 'bank', 'bank_acc', 'mobile', 'email', 'address', 'emergency_contact_name', 'emergency_contact_number', 'emergency_contact_relationship']:
                    field.disabled = True

            self.fields['last_date'].widget = HiddenInput()
            self.fields['is_active'].widget = HiddenInput()
        else:
            for name, field in self.fields.items():
                if name in ['last_name', 'first_name', 'date_joined', 'salary', 'department', 'title', 'grade']:
                    field.disabled = True

    def clean(self):
        data = super().clean()
        if not data['is_active'] and not data['last_date']:
            raise ValidationError(
                'Last date is needed if staff is inactive.')
        return super().clean()


class AcademicRecordForm(ModelForm):
    class Meta:
        model = AcademicRecord
        fields = '__all__'
        widgets = {
            'date_start': DateInput(),
            'date_end': DateInput(),
        }

    def clean_year_completed(self):
        year_completed = self.cleaned_data['year_completed']
        max_year = datetime.date.today().year
        if int(year_completed) > max_year:
            raise ValidationError(
                'Completed year is larger than current year.')
        return year_completed


class AcademicRecordFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AcademicRecordFormsetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Row(
                Column(Field('date_start'),
                       css_class='col-sm-1'),
                Column(Field('date_end'),
                       css_class='col-sm-1'),
                Column(Field('institution_name'),
                       css_class='col-sm-4'),
                Column(Field('qualification'),
                       css_class='col-sm-4'),
                Column(Field('year_completed'),
                       css_class='col-md-1'),
                Column(HTML('''<a role="button" class="fas fa-minus-circle text-danger minus-ar-btn" style="font-size:1.5rem; padding-top:45px;"></a>'''),
                       css_class='col-md-1 text-center'),
                'user',
                'id',
                'DELETE',
                css_class='form-row academic-record-formset'
            ),
        )


class EmploymentHistoryForm(ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = '__all__'
        widgets = {
            'date_start': DateInput(),
            'date_end': DateInput(),
        }


class EmploymentHistoryFormsetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(EmploymentHistoryFormsetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Row(
                Column(Field('date_start'),
                       css_class='col-sm-1'),
                Column(Field('date_end'),
                       css_class='col-sm-1'),
                Column(Field('employer_name'),
                       css_class='col-sm-3'),
                Column(Field('position'),
                       css_class='col-sm-2'),
                Column(Field('reason'),
                       css_class='col-md-4'),
                Column(HTML('''<a role="button" class="fas fa-minus-circle text-danger minus-eh-btn" style="font-size:1.5rem; padding-top:45px;"></a>'''),
                       css_class='col-md-1 text-center'),
                'user',
                'id',
                css_class='form-row employment-history-formset'
            ),
        )
