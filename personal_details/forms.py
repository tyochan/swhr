from django.forms import ModelForm
from django import forms
from .models import Employee

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class CrispyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class EmployeeForm(CrispyForm):
    class Meta:
        model = Employee
        fields = '__all__'
        # exclude = ['staff_no']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column(Field('staff_no', readonly=True),
                       css_class='form-group col-md-1'),
                Column('first_name', css_class='form-group col-md-2'),
                Column('last_name', css_class='form-group col-md-2'),
                Column('start_date', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Row(
                Column('phone_no', css_class='form-group col-md-2'),
                Column('email', css_class='form-group col-md-2'),
                Column('department', css_class='form-group col-md-3'),
                css_class='form-row'
            ),
            Field('address', css_class="form-group col-md-7"),
            Row(
                Column('bank_acc', css_class='form-group col-md-3'),
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
        self.fields['start_date'].widget = forms.DateInput(format='%d-%m-%Y')

        # Rename display fields' names
        self.fields['staff_no'].label = "Employee ID"
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['start_date'].label = "Date Joined"
        self.fields['phone_no'].label = "Phone No"
        self.fields['bank_acc'].label = "Bank Account"
        self.fields['annual_leave'].label = "Annual Leave"


class EmployeeUpdateForm(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")


class EmployeeDeleteForm(EmployeeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeDeleteForm, self).__init__(*args, **kwargs)
