from django.forms import ModelForm, ValidationError, DateInput, ModelChoiceField, HiddenInput, NumberInput

# Models
from .models import Payment
from personal_details.models import User

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText

# Utils
import datetime
import calendar


class PaymentForm(ModelForm):
    user = ModelChoiceField(label='Employee', queryset=User.objects.filter(
        is_staff=False, is_active=True))

    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'period_start': DateInput(attrs={'readonly': True}),
            'period_end': DateInput(attrs={'readonly': True}),
            'unused_leave_days': HiddenInput(),
            'unused_leave_pay': HiddenInput(),
            'is_last': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
            <div class="form-row">
                <div class="col-md-3">
                    <label class="col-form-label font-weight-bold text-info">General</label>
            '''),
            Field('user', css_class='form-group col-md-12'),
            Row(
                Column(AppendedText('unused_leave_days', 'Days', readonly=True),
                       css_class='col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('period_start', css_class='form-group col-md-6'),
                Column('period_end', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('pay_date', css_class='form-group col-md-6'),
                Column('method', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('status', css_class='form-group col-md-6'),
                Column(PrependedText(
                    'net_pay', '$', css_class="font-weight-bold two-decimal", readonly=True), css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            HTML('''
                </div>
                <div class="col-md-9">
                    <div class="form-row">
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-success">
                            <label class="col-form-label font-weight-bold text-success">Payments</label>
            '''),
            PrependedText('basic_salary', '$',
                          css_class="payment two-decimal", readonly=True),
            PrependedText('unused_leave_pay', '$',
                          css_class="payment two-decimal"),
            PrependedText('allowance', '$', css_class="payment two-decimal"),
            PrependedText('other_payments', '$',
                          css_class="payment two-decimal"),
            PrependedText('total_payments', '$',
                          css_class="two-decimal", readonly=True),
            HTML('''
                        </div>
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-danger">
                            <label class="col-form-label font-weight-bold text-danger">Deductions</label>

            '''),
            PrependedText('mpf_employee', '$',
                          css_class="deduction two-decimal", readonly=True),
            PrependedText('np_leave', '$', css_class="deduction two-decimal"),
            PrependedText('other_deductions', '$',
                          css_class="deduction two-decimal"),
            PrependedText('total_deductions', '$',
                          css_class="two-decimal", readonly=True),
            HTML('''
                        </div>
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-secondary">
                            <label class="col-form-label font-weight-bold text-secondary"> Others </label>
            '''),
            PrependedText('mpf_employer', '$',
                          css_class="two-decimal", readonly=True),
            HTML('''
                        </div>
                    </div>
                </div>
            </div>
            '''),
            Field('is_last'),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'payroll:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Init field data
        date = datetime.date.today()  # datetime.date(2018, 12, 18)
        period_start = date.replace(day=1)
        period_end = date.replace(day=calendar.monthrange(
            period_start.year, period_start.month)[1])
        self.fields['period_start'].initial = period_start
        self.fields['period_end'].initial = period_end
        self.fields['pay_date'].initial = date

        self.fields['status'].disabled = True


class PaymentCreateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        # Check for overlapping payment
        payment = Payment.objects.filter(user=data['user'],
                                         period_start__lte=data['period_end'],
                                         period_end__gte=data['period_start']).exclude(status="CC")
        if (payment):
            raise ValidationError(
                'Payment overlapping with [%(payment)s]', params={'payment': payment[0]})
        return data


class PaymentDetailForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True


class PaymentUpdateForm(PaymentDetailForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(PaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(-1, HTML(
            '<a target="_blank" class="btn btn-outline-info" role="button" id="id_export_pdf">Export PDF</a> '))
        if self.user.is_superuser:
            self.helper.layout.insert(-1, Submit('cancel',
                                                 'Cancel', css_class='btn-outline-danger'))


class LastPaymentForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentForm, self).__init__(*args, **kwargs)

        self.helper.layout[2].insert(0, HTML("""
                    <div class="formColumn form-group col-md-6">
                        <label class="col-form-label">Date Joined</label>
                        <input type="text" name="date_joined" class="dateinput form-control" id="id_date_joined" value="{{date_joined|date:"Y-m-d"}}" autocomplete="off" readonly>
                    </div>
                """),
                                     ),

        self.fields['period_end'].widget = DateInput(
            attrs={'readonly': False})
        self.fields['unused_leave_days'].widget = NumberInput(
            attrs={'class': 'one-decimal'})
        self.fields['unused_leave_pay'].widget = NumberInput(
            attrs={'class': 'two-decimal'})

        self.fields['is_last'].initial = True


class LastPaymentCreateForm(LastPaymentForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        # Check for overlapping payment
        payment = Payment.objects.filter(user=data['user'],
                                         period_start__lte=data['period_end'],
                                         period_end__gte=data['period_start'])
        if (payment):
            raise ValidationError(
                'Payment overlapping with [%(payment)s]', params={'payment': payment[0]})

        return data


class LastPaymentDetailForm(LastPaymentForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True


class LastPaymentUpdateForm(LastPaymentDetailForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout.insert(-1, HTML(
            '<a target="_blank" class="btn btn-outline-info" role="button" id="id_export_pdf">Export PDF</a> '))
        self.helper.layout.insert(-1, Submit('cancel',
                                             'Cancel', css_class='btn-outline-danger'))
