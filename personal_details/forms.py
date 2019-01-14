from django.forms import ModelForm, ValidationError, DateInput, TextInput, PasswordInput, NumberInput, HiddenInput, CharField, ChoiceField
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import hashers
from . import choices
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

# Models
from .models import User, TitleRecord, SalaryRecord, AcademicRecord

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class UserForm(ModelForm):
    spouse_name = CharField(label='Spouse Name', required=False)
    spouse_identity_type = ChoiceField(
        label='Identity Type', choices=choices.IDENTITY_TYPE, required=False)
    spouse_identity_no = CharField(label='Identity No.', required=False)

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
            <div class="form-row">
                <div class="col-md-4">
                    <label class="col-form-label font-weight-bold text-info">Basic Info</label>
            '''),
            Field('username', readonly=True),
            Field('password', readonly=True),
            Row(
                Column(Field('staff_id', readonly=True),
                       css_class='form-group col-sm-3'),
                Column(Field('last_name'),
                       css_class='form-group col-md-3'),
                Column(Field('first_name'),
                       css_class='form-group col-md-3'),
                Column('nick_name', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('birth_date'),
                       css_class='form-group col-md-4'),
                Column(Field('identity_type'),
                       css_class='form-group col-md-3'),
                Column(Field('identity_no'),
                       css_class='form-group col-md-5'),
                css_class='form-row'
            ),
            Row(
                Column(AppendedText('annual_leave', 'Days'),
                       css_class='form-group col-md-4'),
                Column('date_joined', css_class='form-group col-md-3'),
                Column('last_date', css_class='form-group col-md-3'),
                Column(PrependedText('is_active', ''),
                       css_class='form-group col-md-1'),
                css_class='form-row'
            ),
            HTML(
                '''<label class="col-form-label font-weight-bold text-warning">Pay Info</label>'''),
            Row(
                Column('bank', css_class='form-group col-md-12'),

                css_class='form-row'
            ),
            Row(
                Column('bank_acc', css_class='form-group col-md-4'),
                Column(PrependedText('salary', '$'),
                       css_class='form-group col-md-4'),
                Column('salary_grade', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            HTML('''
                </div>
                <div class="col-md-1"></div>
                <div class="col-md-7">
                    <label class="col-form-label font-weight-bold text-success">Contact Info</label>
            '''),
            Row(
                Column(Field('mobile'),
                       css_class='form-group col-sm-3'),
                Column(Field('email'),
                       css_class='form-group col-sm-4'),
                css_class='form-row'
            ),
            Row(
                Column(Field('department'),
                       css_class='form-group col-sm-3'),
                Column(Field('title'),
                       css_class='form-group col-sm-3'),
                Column(Field('title_grade'),
                       css_class='form-group col-sm-3'),
                css_class='form-row'
            ),
            Row(
                Column(Field('address'),
                       css_class='form-group col-sm-11'),
            ),
            Row(
                Column(Field('marital_status'),
                       css_class='form-group col-sm-2'),
                Column(Field('spouse_name'),
                       css_class='form-group col-sm-3'),
                Column(Field('spouse_identity_type'),
                       css_class='form-group col-sm-2'),
                Column(Field('spouse_identity_no'),
                       css_class='form-group col-sm-3'),
                css_class='form-row'
            ),
            HTML(
                '''<label class="col-form-label font-weight-bold text-danger">Emergency Contact</label>'''),
            Row(
                Column(Field('emergency_contact_name'),
                       css_class='form-group col-md-3'),
                Column(Field('emergency_contact_number'),
                       css_class='form-group col-md-3'),
                Column(Field('emergency_contact_relationship'),
                       css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            HTML('''
                </div>
            </div>
            '''),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'personal_details:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>')
        )

        # Required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        data = super().clean()
        print(data)
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

        self.fields['password'].widget = PasswordInput(
            attrs={'value': '******'})
        self.fields['password'].disabled = True
        self.fields['date_joined'].disabled = True

        if not self.user.is_superuser:
            self.helper.layout.insert(-1, HTML(
                '<a href="{% url \'change_password\' %}" class="btn btn-outline-info" role="button">Change Password</a> '))
            self.helper.layout.pop(-1)

            self.fields['last_name'].disabled = True
            self.fields['first_name'].disabled = True
            # self.fields['salary'].disabled = True
            self.fields['annual_leave'].disabled = True
            self.fields['last_date'].disabled = True
            self.fields['is_active'].disabled = True

            self.fields['last_date'].widget = HiddenInput()
            self.fields['is_active'].widget = HiddenInput()

    def clean(self):
        data = super().clean()
        if not data['is_active'] and not data['last_date']:
            raise ValidationError(
                'Last date is needed if staff is inactive.')
        return super().clean()


class SalaryForm(ModelForm):
    class Meta:
        model = SalaryRecord
        fields = '__all__'
        widgets = {
            'date_changed': DateInput(),
            'user': HiddenInput(),
            'amount': NumberInput(attrs={'class': 'two-decimal'}),
        }


class SalaryFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SalaryFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Row(
                Column(Field('date_changed'),
                       css_class='form-group col-sm-4'),
                Column(PrependedText('amount', '$'),
                       css_class='form-group col-md-4'),
                Column(Field('grade'),
                       css_class='form-group col-md-4'),
                Column('user', css_class='form-group col-md-1'),
                css_class='form-row'
            ),
        )
        self.render_required_fields = True


SalaryInlineFormSet = inlineformset_factory(
    User, SalaryRecord, form=SalaryForm, fields='__all__', extra=1)
