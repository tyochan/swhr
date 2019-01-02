from django.forms import ModelForm, ValidationError, DateInput, ModelChoiceField, HiddenInput, NumberInput

# Models
from .models import Payment
from personal_details.models import Employee

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText

# Utils
import datetime
import calendar


class PaymentForm(ModelForm):
    employee = ModelChoiceField(queryset=Employee.objects.filter(active=True))

    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            HTML('''
            <div class="form-row">
                <div class="col-md-3">
                    <label class="col-form-label font-weight-bold text-info">General</label>
            '''),
            Field('employee', css_class='form-group col-md-12'),
            Row(
                Column(AppendedText('leaves_unused', 'Days', readonly=True, display='none'),
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
                    'net_pay', '$', css_class="font-weight-bold"), css_class='form-group col-md-6'),
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
            PrependedText('basic_salary', '$', css_class="payment"),
            PrependedText('allowance', '$', css_class="payment"),
            PrependedText('leaves_compensation', '$', css_class="payment"),
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
            Field('last'),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'payroll:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Modify widget
        self.fields['period_start'].widget = DateInput(
            attrs={'readonly': True})
        self.fields['period_end'].widget = DateInput(
            attrs={'readonly': True})
        self.fields['leaves_unused'].widget = HiddenInput()
        self.fields['leaves_compensation'].widget = HiddenInput()
        self.fields['last'].widget = HiddenInput()

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

        self.fields['status'].disabled = True


class PaymentCreateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        print(data)
        # Check for overlapping payment
        payment = Payment.objects.filter(employee=data['employee'],
                                         period_start__lte=data['period_end'],
                                         period_end__gte=data['period_start'])
        print(payment)
        if (payment):
            raise ValidationError(
                'Payment overlapping with [%(payment)s]', params={'payment': payment[0]})

        return data


class PaymentUpdateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout[-2] = HTML(
            '<a target="_blank" class="btn btn-outline-info" role="button" id="id_export_pdf">Export PDF</a> ')
        self.helper.layout.insert(-1, Submit('cancel',
                                             'Cancel', css_class='btn-outline-danger'))

        for name, field in self.fields.items():
            field.disabled = True


class PaymentDetailForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True


class LastPaymentCreateForm(PaymentCreateForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LastPaymentCreateForm, self).__init__(*args, **kwargs)

        self.helper.layout[2].insert(0, HTML("""
                    <div class="formColumn form-group col-md-6">
                        <label class="col-form-label">Join Date</label>
                        <input type="text" name="join_date" class="dateinput form-control" id="id_join_date" value="{{join_date|date:"Y-m-d"}}" autocomplete="off" readonly>
                    </div>
                """),
                                     ),

        self.fields['period_end'].widget = DateInput(
            attrs={'readonly': False})
        self.fields['leaves_unused'].widget = NumberInput()
        self.fields['leaves_compensation'].widget = NumberInput()

        self.fields['last'].initial = True

        self.fields['leaves_unused'].label = "Leaves Unused"
        self.fields['leaves_compensation'].label = "Leaves Compensation"


class LastPaymentUpdateForm(LastPaymentCreateForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout[-2] = HTML(
            '<a target="_blank" class="btn btn-outline-info" role="button" id="id_export_pdf">Export PDF</a> ')
        self.helper.layout.insert(-1, Submit('cancel',
                                             'Cancel', css_class='btn-outline-danger'))

        for name, field in self.fields.items():
            field.disabled = True


class LastPaymentDetailForm(LastPaymentCreateForm):
    def __init__(self, *args, **kwargs):
        super(LastPaymentDetailForm, self).__init__(*args, **kwargs)
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True
