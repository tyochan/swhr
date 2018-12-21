from django.forms import ModelForm, ValidationError, DateInput

# Models
from .models import Employee

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        # exclude = ['staff_no']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column(Field('staff_no', readonly=True),
                       css_class='form-group col-sm-1'),
                Column('last_name', css_class='form-group col-md-2'),
                Column('first_name', css_class='form-group col-md-2'),
                Column('join_date', css_class='form-group col-md-1'),
                Column('leave_date', css_class='form-group col-md-1'),
                Column(PrependedText('active', ''),
                       css_class='form-group col-md-1'),
                css_class='form-row'
            ),
            Row(
                Column('phone_no', css_class='form-group col-md-2'),
                Column('email', css_class='form-group col-md-2'),
                Column('department', css_class='form-group col-md-3'),
                Column('title', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Field('address', css_class="form-group col-md-9"),
            Row(
                Column('bank', css_class='form-group col-md-3'),
                Column('bank_acc', css_class='form-group col-md-2'),
                Column(PrependedText('salary', '$'),
                       css_class='form-group col-md-2'),
                Column(AppendedText('annual_leave', 'Days'),
                       css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'personal_details:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>')
        )

        # Modify widget
        self.fields['join_date'].widget = DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off'})
        self.fields['leave_date'].widget = DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off'})

        # Rename display fields' names
        self.fields['staff_no'].label = "Staff ID"
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['join_date'].label = "Date Joined"
        self.fields['leave_date'].label = "Date Left"
        self.fields['phone_no'].label = "Phone No"
        self.fields['bank_acc'].label = "Bank Account"
        self.fields['annual_leave'].label = "Annual Leave"

    def clean(self):
        data = super().clean()
        print(data)
        if not data['active']:
            if not data['leave_date']:
                raise ValidationError(
                    'Leave date is needed if staff is not active.')

        return super().clean()


class EmployeeUpdateForm(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")
