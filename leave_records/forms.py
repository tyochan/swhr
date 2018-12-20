from django.forms import ModelForm, ValidationError
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
                Column('employee', css_class='form-group col-md-3'),
                Column('day_type', css_class='form-group col-md-1', readonly=True),
                Column('start_date', css_class='form-group col-md-1'),
                Column('end_date', css_class='form-group col-md-1'),
                css_class='form-row'
            ),
            Row(
                Column(AppendedText('spend', 'Days', readonly=True),
                       css_class='form-group col-md-2'),
                Column(Field('type'),
                       css_class='form-group col-md-2'),
                Column('status', css_class="form-group col-md-2"),
                css_class='form-row'
            ),
            Row(
                Column('remarks', css_class="form-group col-md-6"),

                css_class='form-row',
            ),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'leave_records:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Modify widget
        self.fields['start_date'].widget = forms.DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off'})
        self.fields['end_date'].widget = forms.DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off'})
        # self.fields['from_time'].widget = forms.TimeInput(
        #     format='%H:%M', attrs={'class': 'timepicker', 'onkeydown': 'return false', 'autocomplete': 'off'})
        # self.fields['to_time'].widget = forms.TimeInput(
        #     format='%H:%M', attrs={'class': 'timepicker', 'onkeydown': 'return false', 'autocomplete': 'off'})
        self.fields['remarks'].widget = forms.Textarea()

        # Rename display fields' names
        self.fields['start_date'].label = "Start Date"
        self.fields['end_date'].label = "End Date"
        # self.fields['from_time'].label = "From Time"
        # self.fields['to_time'].label = "To Time"
        self.fields['spend'].label = "Days Spend"
        self.fields['day_type'].label = "Day Type"

        self.fields['status'].disabled = True


class LeaveCreateForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        print(data)
        if data["spend"]:
            # Check if leave exists quota
            if data["type"] == 'AL':
                if data["spend"] > data["employee"].annual_leave:
                    raise ValidationError(
                        'Leave exceeds your quota: %(quota)s days.', params={'quota': data["employee"].annual_leave})
            leaves = Leave.objects.filter(employee=data["employee"], start_date__lte=data["end_date"], end_date__gte=data["start_date"]).exclude(
                status="RE")
            for l in leaves:
                # Leave starts and ends on same day
                if "day_type" in data:
                    if data["day_type"] == 'HD':  # Half day leaves
                        count = Leave.objects.exclude(
                            status="RE").filter(
                            start_date=data["start_date"]).count()
                        if count >= 2:
                            raise ValidationError(
                                'Leaves already applied for: %(date)s', params={'date': data["start_date"]}
                            )
                    else:  # Full day leaves
                        raise ValidationError(
                            'Leave overlaps with applied leave: %(leave)s', params={'leave': l})
                else:  # Full day leaves
                    raise ValidationError(
                        'Leave overlaps with applied leave: %(leave)s', params={'leave': l})

        return super().clean()


class LeaveUpdateForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout[-2] = Submit('approve',
                                        'Approve', css_class="btn-outline-primary")
        self.helper.layout.insert(-1, Submit('reject',
                                             'Reject', css_class='btn-outline-danger'))

        for name, field in self.fields.items():
            field.disabled = True


class LeaveDetailForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True
