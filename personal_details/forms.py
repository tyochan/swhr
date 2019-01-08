from django.forms import ModelForm, ValidationError, DateInput, TextInput, PasswordInput, NumberInput, HiddenInput
from django.contrib.auth import hashers

# Models
from .models import User

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class UserForm(ModelForm):
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
            'salary': NumberInput(attrs={'class': 'two-decimal'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
            <div class="form-row">
                <div class="col-md-3">
                    <label class="col-form-label font-weight-bold text-info">Login Details</label>
            '''),
            Row(
                Column(Field('username', readonly=True),
                       css_class='form-group col-sm-6'),
                Column('password', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column(Field('last_name'),
                       css_class='form-group col-md-6'),
                Column(Field('first_name'),
                       css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Field('nick_name', css_class='form-group col-md-6'),
            HTML('''
                </div>
                <div class="col-md-1"></div>
                <div class="col-md-8">
                    <label class="col-form-label font-weight-bold text-secondary">Profile</label>
            '''),
            Row(
                Column(Field('staff_id', readonly=True),
                       css_class='form-group col-sm-2'),
                Column(Field('mobile'),
                       css_class='form-group col-sm-3'),
                Column(Field('email'),
                       css_class='form-group col-sm-5'),
                css_class='form-row'
            ),
            Row(
                Column('department', css_class='form-group col-md-5'),
                Column('title', css_class='form-group col-md-5'),
                css_class='form-row'
            ),
            Field('address', css_class="form-group col-md-10"),
            Row(
                Column('bank', css_class='form-group col-md-6'),
                Column('bank_acc', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column(PrependedText('salary', '$'),
                       css_class='form-group col-md-2'),
                Column(AppendedText('annual_leave', 'Days'),
                       css_class='form-group col-md-2'),
                Column('date_joined', css_class='form-group col-md-2'),
                Column('last_date', css_class='form-group col-md-2'),
                Column(PrependedText('is_active', ''),
                       css_class='form-group col-md-1'),
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
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")

        self.fields['password'].widget = PasswordInput(
            attrs={'value': '******'})
        self.fields['password'].disabled = True
        self.fields['date_joined'].disabled = True

    def clean(self):
        data = super().clean()
        if not data['is_active'] and not data['last_date']:
            raise ValidationError(
                'Last date is needed if staff is inactive.')
        return super().clean()


class NormalUserUpdateForm(UserUpdateForm):
    def __init__(self, *args, **kwargs):
        super(NormalUserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['last_name'].disabled = True
        self.fields['first_name'].disabled = True
        self.fields['salary'].disabled = True
        self.fields['annual_leave'].disabled = True
        self.fields['last_date'].disabled = True
        self.fields['is_active'].disabled = True

        self.fields['last_date'].widget = HiddenInput()
        self.fields['is_active'].widget = HiddenInput()
