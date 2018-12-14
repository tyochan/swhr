from django.forms import ModelForm, ValidationError
from django import forms
from .models import Payment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class CrispyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CrispyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)


class PaymentForm(CrispyForm):

    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('employee', css_class='form-group col-md-3'),
                Column('period_start', css_class='form-group col-md-1'),
                Column('period_end', css_class='form-group col-md-1'),
                Column('method', css_class='form-group col-md-1'),
                css_class='form-row'
            ),
            Row(
                HTML('''
                    <div class="formColumn form-group col-md-2">
                      <div id="" class="form-group"> <label for="" class="col-form-label  requiredField">
                          Basic Salary</label>
                        <div class="">
                          <div class="input-group">
                            <div class="input-group-prepend">
                            <span class="input-group-text">$</span>
                            </div>
                            <input type="number" class="numberinput form-control" id="id_basic_salary" readonly=True>
                          </div>
                        </div>
                      </div>
                    </div>
                '''),
                Column(PrependedText('mpf_employer', '$'),
                       css_class='form-group col-md-2'),
                Column(PrependedText('mpf_employee', '$'),
                       css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            Row(
                Column(PrependedText('net_pay', '$'),
                       css_class="form-group col-md-2"),
                Column('pay_date', css_class='form-group col-md-1'),
                # Column('status', css_class="form-group col-md-2", readonly=True),
                css_class='form-row',
            ),
            Submit('submit', 'Save', css_class="btn-outline-primary"),
            HTML(
                '<a href="{% url \'payroll:index\' %}" class="btn btn-outline-secondary" role="button">Back</a>'),
        )

        # Modify widget
        self.fields['period_start'].widget = forms.DateInput(
            format='Y-m-d', attrs={'class': 'datepicker', 'onkeydown': 'return false', 'autocomplete': 'off'})
        self.fields['period_end'].widget = forms.DateInput(
            format='Y-m-d', attrs={'class': 'datepicker', 'onkeydown': 'return false', 'autocomplete': 'off'})
        self.fields['pay_date'].widget = forms.DateInput(
            format='Y-m-d', attrs={'class': 'datepicker', 'onkeydown': 'return false', 'autocomplete': 'off'})

        # Rename display fields' names
        self.fields['period_start'].label = "Period Start"
        self.fields['period_end'].label = "Period End"
        self.fields['pay_date'].label = "Pay Date"
        self.fields['method'].label = "Pay Method"

        # self.fields['status'].disabled = True


class PaymentCreateForm(PaymentForm):
    def __init__(self, *args, **kwargs):
        super(PaymentCreateForm, self).__init__(*args, **kwargs)


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
        self.helper.layout.pop(-2)

        for name, field in self.fields.items():
            field.disabled = True
