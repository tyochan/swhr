from django.forms import ModelForm, ValidationError, DateInput, Textarea, ModelChoiceField, NumberInput

# Models
from .models import Leave
from personal_details.models import User

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText


class LeaveForm(ModelForm):
    user = ModelChoiceField(
        label='Employee',
        queryset=User.objects.filter(is_active=True, is_staff=False)
    )

    class Meta:
        model = Leave
        fields = '__all__'
        widgets = {
            'remarks': Textarea(),
            'spend': NumberInput(attrs={'class': 'one-decimal'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(LeaveForm, self).__init__(*args, **kwargs)
        if not self.user.is_superuser:
            self.fields['user'].queryset = User.objects.filter(id=self.user.id)
            self.fields['user'].initial = self.user.id
            self.fields['user'].disabled = True

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
                <div class="container col-sm-6 mt-3">
            '''),
            Row(
                Column('user', css_class='col-md-4'),
                Column('day_type', css_class='col-md-2'),
                Column('start_date', css_class='col-md-3'),
                Column('end_date', readonly=True, css_class='col-md-3'),
                css_class='form-row'
            ),
            Row(
                Column(
                    AppendedText('spend', 'Days', readonly=True),
                    css_class='col-md-4'
                ),
                Column('type', css_class='col-md-4'),
                Column('status', css_class='col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('remarks', css_class="col-md-12"),
                css_class='form-row',
            ),
            Submit(
                'submit', 'Save', css_class="btn-outline-primary"
            ),
            HTML(
                '<a href="{% url \'leave_records:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
            HTML('''
                </div>
            '''),
        )

        # Avaliabiility of field (can't enable by js if disabled)
        self.fields['status'].disabled = True


class LeaveCreateForm(LeaveForm):
    def clean(self):
        data = super().clean()

        # Leave > Quota
        if data['spend'] > data['user'].annual_leave:
            raise ValidationError(
                f'Leave exceeds current quota of {data["user"].annual_leave} days.')

        if 'AL' in data['type']:
            leaves = Leave.objects.filter(
                user=data["user"], start_date__lte=data["end_date"],
                end_date__gte=data["start_date"]
            ).exclude(status="RE")

            for obj in leaves:
                if 'HD' in data['day_type']:  # Half day leaves
                    if Leave.objects.filter(start_date=data["start_date"]).exclude(status="RE").count() >= 2:
                        raise ValidationError(
                            f'Leaves have been taken for {data["start_date"]}')

                else:  # Full day leaves
                    raise ValidationError(
                        f'Leave overlapping with {obj}')

        return data


class LeaveDetailForm(LeaveForm):
    def __init__(self, *args, **kwargs):
        super(LeaveDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-3)  # pop save button

        for name, field in self.fields.items():
            field.disabled = True


class LeaveUpdateForm(LeaveDetailForm):
    def __init__(self, *args, **kwargs):
        super(LeaveUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(-2, Submit('approve',
                                             'Approve', css_class="btn-outline-primary"))
        self.helper.layout.insert(-2, Submit('reject',
                                             'Reject', css_class='btn-outline-danger'))
