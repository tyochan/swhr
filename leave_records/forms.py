from django.forms import ModelForm
from django import forms
from .models import Leave

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class CrispyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class LeaveForm(CrispyForm):
    class Meta:
        model = Leave
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column(Field('serial_no', readonly=True),
                       css_class='form-group col-md-1'),
                Column('employee', css_class='form-group col-md-3'),
                Column('start_date', css_class='form-group col-md-1'),
                Column('end_date', css_class='form-group col-md-1'),
                css_class='form-row'
            ),
            Row(
                Column('from_time', css_class='form-group col-md-1'),
                Column('to_time', css_class='form-group col-md-1'),
                Column(AppendedText('spend', 'Days'),
                       css_class='form-group col-md-2'),
                Column(Field('type'),
                       css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Row(
                Column('remarks', css_class="form-group col-md-4"),
                Column('status', css_class="form-group col-md-2"),
                css_class='form-row',
            ),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'leave_records:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Modify widget
        self.fields['start_date'].widget = forms.DateInput(
            format='%Y-%m-%d', attrs={'class': 'datepicker', 'onkeydown': 'return false'})
        self.fields['end_date'].widget = forms.DateInput(
            format='%Y-%m-%d', attrs={'class': 'datepicker', 'onkeydown': 'return false'})
        self.fields['from_time'].widget = forms.TimeInput(
            format='%H:%M', attrs={'class': 'timepicker', 'onkeydown': 'return false'})
        self.fields['to_time'].widget = forms.TimeInput(
            format='%H:%M', attrs={'class': 'timepicker', 'onkeydown': 'return false'})
        self.fields['remarks'].widget = forms.Textarea()

        # Rename display fields' names
        self.fields['start_date'].label = "Start Date"
        self.fields['end_date'].label = "End Date"
        self.fields['from_time'].label = "From Time"
        self.fields['to_time'].label = "To Time"
        self.fields['spend'].label = "Days Spend"

        self.fields['status'].disabled = True


class LeaveUpdateForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit, 'Update', css_class="btn-outline-primary")

        for name, field in self.fields.items():
            if field == self.fields['status'] or field == self.fields['spend']:
                field.disabled = False
            else:
                field.disabled = True
