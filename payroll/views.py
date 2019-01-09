# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Models
from .models import Payment
from django.db.models import Q
from leave_records.models import Leave
from personal_details.models import User

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Utils
import datetime
import calendar
from swhr import constant
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
from django_weasyprint import WeasyTemplateResponseMixin
from . import choices
from swhr import utils


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'payroll.html'
    context_object_name = 'payments'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-period_start')
        if self.request.user.is_superuser:
            # Filtering
            staff_id = self.request.GET.get('staff_id', '')
            name = self.request.GET.get('name', '')
            status = self.request.GET.get('status', '')
            is_last = bool(self.request.GET.get('is_last', ''))

            if bool(staff_id + name + status + self.request.GET.get('is_last', '')):

                print('Payment Filtering: %s %s %s %s' %
                      (staff_id, name, status, is_last))

                return Payment.objects.order_by(order_by).filter(Q(user__staff_id__contains=staff_id),
                                                                 Q(user__last_name__contains=name)
                                                                 | Q(user__first_name__contains=name),
                                                                 Q(status__contains=status),
                                                                 Q(is_last=is_last),)
            else:
                return Payment.objects.order_by(order_by)
        else:
            return Payment.objects.order_by(order_by).filter(user__id=self.request.user.id).exclude(status='CC')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-period_start')

        # Filtering
        context['staff_id'] = self.request.GET.get('staff_id', '')
        context['name'] = self.request.GET.get('name', '')
        context['status'] = self.request.GET.get('status', '')
        context['is_last'] = self.request.GET.get('is_last', '')

        context['is_last_options'] = dict(
            {'': 'Monthly Payment', 'True': 'Last Payment'})
        context['status_options'] = dict((key, val)
                                         for key, val in choices.STATUS_CHOICES)
        context['filter'] = 'staff_id=%s&name=%s&status=%s&is_last=%s' % (
            context['staff_id'], context['name'], context['status'], context['is_last'])

        return context


class PaymentCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.PaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')
    permission_required = 'payroll.create_payment'


class PaymentUpdateView(UserPassesTestMixin, UpdateView):
    form_class = forms.PaymentUpdateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Updating payment status
    def form_valid(self, form):
        payment = Payment.objects.get(id=self.kwargs['pk'])
        if 'cancel' in self.request.POST:
            payment.status = 'CC'
            payment.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        payment = self.get_object()
        return (payment.user.id == self.request.user.id or self.request.user.is_superuser) and payment.status == 'PA'


class PaymentDetailView(UserPassesTestMixin, UpdateView):
    form_class = forms.PaymentDetailForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    def test_func(self):
        payment = self.get_object()
        return payment.user.id == self.request.user.id or self.request.user.is_superuser


class PaymentPDFView(UserPassesTestMixin, DetailView, WeasyTemplateResponseMixin):
    model = Payment
    context_object_name = 'p'
    template_name = 'payslip_pdf.html'
    pdf_filename = 'payslip.pdf'
    pdf_attachment = False

    def test_func(self):
        payment = self.get_object()
        return payment.user.id == self.request.user.id or self.request.user.is_superuser


class LastPaymentCreateView(PermissionRequiredMixin, CreateView):
    form_class = forms.LastPaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')
    permission_required = 'payroll.create_payment'


class LastPaymentUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = forms.LastPaymentUpdateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')
    permission_required = 'payroll.change_payment'

    def get_context_data(self, **kwargs):
        context = super(LastPaymentUpdateView, self).get_context_data(**kwargs)
        context['date_joined'] = context['object'].user.date_joined
        return context

    # Updating payment status
    def form_valid(self, form):
        payment = Payment.objects.get(id=self.kwargs['pk'])
        if 'cancel' in self.request.POST:
            payment.status = 'CC'
            payment.save()
        return HttpResponseRedirect(self.get_success_url())


class LastPaymentDetailView(UserPassesTestMixin, UpdateView):
    form_class = forms.LastPaymentDetailForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    def get_context_data(self, **kwargs):
        context = super(LastPaymentDetailView, self).get_context_data(**kwargs)
        context['date_joined'] = context['object'].user.date_joined
        return context

    def test_func(self):
        payment = self.get_object()
        return payment.user.id == self.request.user.id or self.request.user.is_superuser


class LastPaymentPDFView(UserPassesTestMixin, DetailView, WeasyTemplateResponseMixin):
    model = Payment
    context_object_name = 'p'
    template_name = 'payslip_pdf.html'
    pdf_filename = 'last_payslip.pdf'
    pdf_attachment = False

    def test_func(self):
        payment = self.get_object()
        return payment.user.id == self.request.user.id or self.request.user.is_superuser


def limit_period(start_date, end_date, period_start, period_end):
    if start_date < period_start:
        start_date = period_start
    if end_date > period_end:
        end_date = period_end
    return start_date, end_date


def get_mpf(salary, days_passed):
    mpf_employer, mpf_employee = 0, 0

    # less than 3 months no mpf
    if days_passed < 60:
        pass
    else:
        # Employer MPF cumulative for third month
        if 60 <= days_passed < 90:
            payments = Payment.objects.all().filter(user=user,
                                                    period_end__lte=period_start)
            for p in payments:
                if p.net_pay > 30000:
                    mpf_employer += 1500
                else:
                    mpf_employer += p.net_pay * 0.05

        if salary > 30000:
            mpf_employee = 1500
            mpf_employer = 1500
        elif 7100 <= salary <= 30000:
            mpf_employee = salary * 0.05
            mpf_employer = salary * 0.05
        else:
            mpf_employer = salary * 0.05

    return mpf_employer, mpf_employee


@login_required
@ajax
def payment_calculation(request):
    user = User.objects.get(id=request.GET['user_id'])

    # Split and parse string date to int list
    period_start = datetime.datetime.strptime(
        request.GET['period_start'], '%Y-%m-%d')
    period_end = datetime.datetime.strptime(
        request.GET['period_end'], '%Y-%m-%d')
    period_end = period_end.replace(tzinfo=None)
    date_joined = user.date_joined.replace(
        tzinfo=None)  # replace timezone for comparison

    days_passed = (period_end - date_joined).days + 1

    # Max days in this pay period
    temp, period_max = calendar.monthrange(period_end.year, period_end.month)
    # First month
    period_work = days_passed if days_passed < 32 else (
        period_end - period_start).days + 1

    # This month
    leaves = Leave.objects.all().filter(user=user,
                                        start_date__lte=period_end, end_date__gte=period_start, type='NL').exclude(status='RE')
    for l in leaves:
        # Limit leave in within period and Calculate spend days
        spend = utils.period_spend_days(limit_period(
            l.start_date, l.end_date, period_start, period_end))
        period_work -= spend

    ratio = period_work / period_max
    salary = user.salary * ratio
    no_pay_leave = user.salary * (period_max - period_work) / period_max

    # Calculate net pay and mpf
    mpf_employer, mpf_employee = get_mpf(salary, days_passed)

    # Unused Annual Leaves if last payment
    unused_leave_pay, unused_leave_days = 0, 0
    if request.GET['is_last'] == 'True':
        future_leave_days = utils.annual_leave_to_year_end(period_end.date())
        unused_leave_days = user.annual_leave - future_leave_days

    # Total Payment = Basic Salary + Allowance + Others
    total_payments = user.salary + \
        float(request.GET['allowance']) + float(request.GET['other_payments'])

    # Total Deduction = MPF + No Pay Leave + Others
    total_deductions = mpf_employee + no_pay_leave + \
        float(request.GET['other_deductions'])
    net_pay = total_payments - total_deductions
    return {'basic_salary': user.salary, 'mpf_employer': mpf_employer,
            'mpf_employee': mpf_employee, 'net_pay': net_pay, 'no_pay_leave': no_pay_leave,
            'total_payments': total_payments, 'total_deductions': total_deductions,
            'date_joined': user.date_joined.date(), 'unused_leave_days': unused_leave_days,
            'unused_leave_pay': unused_leave_pay}
