from django.forms import ModelForm, ValidationError, DateInput, Textarea, ModelChoiceField

# Models
from .models import Leave
from personal_details.models import Employee

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class LeaveForm(ModelForm):
    employee = ModelChoiceField(queryset=Employee.objects.filter(active=True))

    class Meta:
        model = Leave
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
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
        self.fields['remarks'].widget = Textarea()

        # Rename display fields' names
        self.fields['start_date'].label = "Start Date"
        self.fields['end_date'].label = "End Date"
        self.fields['spend'].label = "Days Spend"
        self.fields['day_type'].label = "Day Type"

        # Avaliabiility of field (can't enable by js if disabled)
        self.fields['status'].disabled = True


class LeaveCreateForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        if data["spend"]:
            # Check if leave exists quota
            if data["type"] == 'AL':
                if data["spend"] > data["employee"].annual_leave:
                    raise ValidationError(
                        'Leave exceeds current quota [%(quota)s days].', params={'quota': data["employee"].annual_leave})
            leaves = Leave.objects.filter(employee=data["employee"],
                                          start_date__lte=data["end_date"],
                                          end_date__gte=data["start_date"]).exclude(status="RE")
            for l in leaves:
                # Leave starts and ends on same day
                if "day_type" in data:
                    if data["day_type"] == 'HD':  # Half day leaves
                        count = Leave.objects.exclude(
                            status="RE").filter(
                            start_date=data["start_date"]).count()
                        if count >= 2:
                            raise ValidationError(
                                'Leaves applied for [%(date)s]', params={'date': data["start_date"]}
                            )
                    else:  # Full day leaves
                        raise ValidationError(
                            'Leave overlapping with [%(leave)s]', params={'leave': l})
                else:  # Full day leaves
                    raise ValidationError(
                        'Leave overlapping with [%(leave)s]', params={'leave': l})
        return data


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
        self.helper.layout.pop(-2)  # pop save button

        for name, field in self.fields.items():
            field.disabled = True
