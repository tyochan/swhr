from django.forms import ModelForm, ValidationError, DateInput

# Models
from .models import Payment

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText

# Utils
import datetime
import calendar


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
            <div class="form-row">
                <div class="col-md-2">
                    <label class="col-form-label font-weight-bold text-info">General</label>
            '''),
            Field('employee', css_class='form-group col-md-12'),
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
            PrependedText('net_pay', '$', css_class="font-weight-bold"),
            HTML('''
                </div>
                <div class="col-md-9">
                    <div class="form-row">
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-success">
                            <label class="col-form-label font-weight-bold text-success">Payments</label>
            '''),
            PrependedText('basic_salary', '$', css_class="payment"),
            PrependedText('allowance', '$', css_class="payment"),
            PrependedText('other_payments', '$', css_class="payment"),
            PrependedText('total_payments', '$', css_class="payment"),
            HTML('''
                        </div>
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-danger">
                            <label class="col-form-label font-weight-bold text-danger">Deductions</label>

            '''),
            PrependedText('mpf_employee', '$', css_class="deduction"),
            PrependedText('np_leave', '$', css_class="deduction"),
            PrependedText('other_deductions', '$', css_class="deduction"),
            PrependedText('total_deductions', '$', css_class="deduction"),
            HTML('''
                        </div>
                        <div class="col-md-1"></div>
                        <div class="formColumn form-group col-md-3 rounded  border-secondary">
                            <label class="col-form-label font-weight-bold text-secondary"> Others </label>
            '''),
            PrependedText('mpf_employer', '$'),
            HTML('''
                        </div>
                    </div>
                </div>
            </div>
            '''),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'payroll:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Modify widget
        self.fields['period_start'].widget = DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off', 'readonly': True})
        self.fields['period_end'].widget = DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off', 'readonly': True})
        self.fields['pay_date'].widget = DateInput(
            attrs={'onkeydown': 'return false', 'autocomplete': 'off'})

        # Rename display fields' names
        self.fields['period_start'].label = "Period Start"
        self.fields['period_end'].label = "Period End"
        self.fields['pay_date'].label = "Pay Date"
        self.fields['method'].label = "Pay Method"
        self.fields['np_leave'].label = "No Pay Leaves"
        self.fields['other_payments'].label = "Others"
        self.fields['other_deductions'].label = "Others"
        self.fields['mpf_employee'].label = "Employee MPF Contribution"
        self.fields['mpf_employer'].label = "Employer MPF Contribution"
        self.fields['total_payments'].label = "Total"
        self.fields['total_deductions'].label = "Total"

        # Init field data
        date = datetime.date.today()  # datetime.date(2018, 12, 18)
        period_start = date.replace(day=1)
        period_end = date.replace(day=calendar.monthrange(
            period_start.year, period_start.month)[1])
        self.fields['period_start'].initial = period_start
        self.fields['period_end'].initial = period_end
        self.fields['pay_date'].initial = date


class PaymentCreateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        # Check for overlapping payment
        payment = Payment.objects.filter(employee=data['employee'],
                                         period_start__lte=data['period_end'],
                                         period_end__gte=data['period_start'])
        if (payment):
            raise ValidationError(
                'Payment overlapping with [%(payment)s]', params={'payment': payment[0]})

        return data


class PaymentUpdateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.filter(Submit).wrap(
            Submit,  'Approve', css_class="btn-outline-primary")
        self.helper.layout.insert(-1, Submit('reject',
                                             'Reject', css_class='btn-outline-danger'))

        for name, field in self.fields.items():
            field.disabled = True


class PaymentDetailForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout[-2] = HTML(
            '<a target="_blank" class="btn btn-outline-info" role="button" id="id_export_pdf">Export PDF</a> ')

        for name, field in self.fields.items():
            field.disabled = True
