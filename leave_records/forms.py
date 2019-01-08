from django.forms import ModelForm, ValidationError, DateInput, Textarea, ModelChoiceField, NumberInput

# Models
from .models import Leave
from personal_details.models import User

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        widgets = {
            'remarks': Textarea(),
            'spend': NumberInput(attrs={'class': 'one-decimal'}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('user', css_class='form-group col-md-3'),
                Column(Field('day_type'),
                       css_class='form-group col-md-1'),
                Column('start_date', css_class='form-group col-md-1'),
                Column(Field('end_date', readonly=True),
                       css_class='form-group col-md-1'),
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

        # Avaliabiility of field (can't enable by js if disabled)
        self.fields['day_type'].disabled = True
        self.fields['status'].disabled = True


class LeaveCreateForm(LeaveForm):
    user = ModelChoiceField(
        label='Employee', queryset=User.objects.filter(is_active=True))

    def __init__(self, *args, **kwargs):
        super(LeaveCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        if data["spend"]:
            # Check if leave exists quota
            if data["type"] == 'AL':
                if data["spend"] > data["user"].annual_leave:
                    raise ValidationError(
                        'Leave exceeds current quota [%(quota)s days].', params={'quota': data["user"].annual_leave})
            leaves = Leave.objects.filter(user=data["user"],
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


class NormalLeaveCreateForm(LeaveCreateForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(NormalLeaveCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'] = ModelChoiceField(
            label='Employee', queryset=User.objects.filter(id=self.user.id))

        self.fields['user'].initial = self.user.id
        self.fields['user'].disabled = True


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
