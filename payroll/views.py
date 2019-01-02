# Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models
from .models import Payment
from django.db.models import Q
from leave_records.models import Leave
from personal_details.models import Employee

# Form classes
from . import forms

# Response
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

# Utils
import datetime
import calendar
from swhr import strings
from django_ajax.decorators import ajax
from django_weasyprint import WeasyTemplateResponseMixin
from . import choices


class IndexView(ListView):
    template_name = 'payroll.html'
    context_object_name = 'payments'
    paginate_by = 13

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-period_start')

        # Filtering
        staff_no = self.request.GET.get('staff_no', '')
        name = self.request.GET.get('name', '')
        status = self.request.GET.get('status', '')
        last = bool(self.request.GET.get('last', ''))
        print('Payment Filtering: %s %s %s %s' %
              (staff_no, name, status, last))

        return Payment.objects.order_by(order_by).filter(Q(employee__staff_no__contains=staff_no),
                                                         Q(employee__last_name__contains=name) |
                                                         Q(employee__first_name__contains=name),
                                                         Q(status__contains=status),
                                                         Q(last=last),)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-period_start')

        # Filtering
        context['staff_no'] = self.request.GET.get('staff_no', '')
        context['name'] = self.request.GET.get('name', '')
        context['status'] = self.request.GET.get('status', '')
        context['last'] = self.request.GET.get('last', '')

        context['last_options'] = dict(
            {'': 'Monthly Payment', 'True': 'Last Payment'})
        context['status_options'] = dict((key, val)
                                         for key, val in choices.STATUS_CHOICES)
        context['filter'] = 'staff_no=%s&name=%s&status=%s&last=%s' % (
            context['staff_no'], context['name'], context['status'], context['last'])

        return context


class PaymentCreateView(CreateView):
    form_class = forms.PaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')


class PaymentUpdateView(UpdateView):
    form_class = forms.PaymentUpdateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    # Updating payment status
    def form_valid(self, form):
        payment = Payment.objects.get(id=self.kwargs['pk'])
        if 'cancel' in self.request.POST:
            payment.status = 'CC'
            payment.save()
        return HttpResponseRedirect("/payroll/")


class PaymentDetailView(UpdateView):
    form_class = forms.PaymentDetailForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')


class PaymentPDFView(DetailView, WeasyTemplateResponseMixin):
    model = Payment
    context_object_name = 'p'
    template_name = 'payslip_pdf.html'
    pdf_filename = 'payslip.pdf'
    pdf_attachment = False


class LastPaymentCreateView(CreateView):
    form_class = forms.LastPaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')


class LastPaymentUpdateView(UpdateView):
    form_class = forms.LastPaymentUpdateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    def get_context_data(self, **kwargs):
        context = super(LastPaymentUpdateView, self).get_context_data(**kwargs)
        context['join_date'] = context['object'].employee.join_date
        return context

    # Updating payment status
    def form_valid(self, form):
        payment = Payment.objects.get(id=self.kwargs['pk'])
        if 'cancel' in self.request.POST:
            payment.status = 'CC'
            payment.save()
        return HttpResponseRedirect("/payroll/")


class LastPaymentDetailView(UpdateView):
    form_class = forms.LastPaymentDetailForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')

    def get_context_data(self, **kwargs):
        context = super(LastPaymentDetailView, self).get_context_data(**kwargs)
        context['join_date'] = context['object'].employee.join_date
        return context


class LastPaymentPDFView(DetailView, WeasyTemplateResponseMixin):
    model = Payment
    context_object_name = 'p'
    template_name = 'last_payslip_pdf.html'
    pdf_filename = 'last_payslip.pdf'
    pdf_attachment = False


@ajax
def calculateSalary(request):
    employee = Employee.objects.get(staff_no=request.GET['staff_no'])

    # Split and parse string date to int list
    period_start = [int(x) for x in request.GET['period_start'].split("-")]
    period_end = [int(x) for x in request.GET['period_end'].split("-")]
    period_start = datetime.date(
        period_start[0], period_start[1], period_start[2])
    period_end = datetime.date(period_end[0], period_end[1], period_end[2])

    # Max days in this pay period
    temp, period_max = calendar.monthrange(period_end.year, period_end.month)
    # First month
    if (period_end - employee.join_date).days < 32:
        period_work = (period_end - employee.join_date).days + 1
    else:
        period_work = (period_end - period_start).days + 1

    # This month
    leaves = Leave.objects.all().filter(employee=employee,
                                        start_date__lte=period_end, end_date__gte=period_start, type='NL').exclude(status='RE')

    for l in leaves:
        # Limit leave in within period
        if l.start_date < period_start:
            l.start_date = period_start
        if l.end_date > period_end:
            l.end_date = period_end

        # Calculate spend days
        spend = (l.end_date - l.start_date).days + 1
        # Weekends
        temp = l.start_date
        while temp < l.end_date + datetime.timedelta(days=1):
            if temp.isoweekday() == 6 or temp.isoweekday() == 7:
                spend -= 1
            temp += datetime.timedelta(days=1)

        # Holidays
        for h in strings.HOLIDAYS:
            date = datetime.datetime.strptime(h, '%Y-%m-%d').date()
            if period_start < date < period_end:
                spend -= 1

        period_work -= spend

    ratio = period_work / period_max
    salary = employee.salary * ratio
    no_pay_leave = employee.salary * (period_max - period_work) / period_max

    # Calculate net pay and mpf
    mpf_employer, mpf_employee, net_pay = 0, 0, 0
    past = (period_end - employee.join_date).days + 1  # Past days from join
    if past < 60:  # less than 3 months no mpf
        net_pay = salary
    elif 60 <= past < 90:  # 3rd month
        payments = Payment.objects.all().filter(employee=employee,
                                                period_end__lte=period_start)
        # Employer MPF cumulative
        for p in payments:
            if p.net_pay > 30000:
                mpf_employer += 1500
            else:
                mpf_employer += p.net_pay * 0.05

        if salary > 30000:
            mpf_employee = 1500
            mpf_employer += 1500
        elif 7100 <= salary <= 30000:
            mpf_employee = salary * 0.05
            mpf_employer += salary * 0.05
        else:
            mpf_employer += salary * 0.05

    else:  # 4th month onwards
        if salary > 30000:
            mpf_employee = 1500
            mpf_employer = 1500
        elif 7100 <= salary <= 30000:
            mpf_employee = salary * 0.05
            mpf_employer = salary * 0.05
        else:
            mpf_employer = salary * 0.05

    total_payments = employee.salary
    total_deductions = mpf_employee + no_pay_leave
    net_pay = total_payments - total_deductions
    return {'basic_salary': employee.salary, 'mpf_employer': mpf_employer,
            'mpf_employee': mpf_employee, 'net_pay': net_pay, 'no_pay_leave': no_pay_leave,
            'total_payments': total_payments, 'total_deductions': total_deductions, }


@ajax
def lastPayment(request):
    employee = Employee.objects.get(staff_no=request.GET['staff_no'])

    # Split and parse string date to int list
    period_start = [int(x) for x in request.GET['period_start'].split("-")]
    period_end = [int(x) for x in request.GET['period_end'].split("-")]
    period_start = datetime.date(
        period_start[0], period_start[1], period_start[2])
    period_end = datetime.date(period_end[0], period_end[1], period_end[2])

    # Max days in this pay period
    temp, period_max = calendar.monthrange(period_end.year, period_end.month)
    # First month
    if (period_end - employee.join_date).days < 32:
        period_work = (period_end - employee.join_date).days + 1
    else:
        period_work = (period_end - period_start).days + 1

    # This month
    leaves = Leave.objects.all().filter(employee=employee,
                                        start_date__lte=period_end, end_date__gte=period_start, type='NL').exclude(status='RE')

    for l in leaves:
        # Limit leave in within period
        if l.start_date < period_start:
            l.start_date = period_start
        if l.end_date > period_end:
            l.end_date = period_end

        # Calculate spend days
        spend = (l.end_date - l.start_date).days + 1
        # Weekends
        temp = l.start_date
        while temp < l.end_date + datetime.timedelta(days=1):
            if temp.isoweekday() == 6 or temp.isoweekday() == 7:
                spend -= 1
            temp += datetime.timedelta(days=1)

        # Holidays
        for h in strings.HOLIDAYS:
            date = datetime.datetime.strptime(h, '%Y-%m-%d').date()
            if period_start < date < period_end:
                spend -= 1

        period_work -= spend

    ratio = period_work / period_max
    salary = employee.salary * ratio
    no_pay_leave = employee.salary * (period_max - period_work) / period_max

    # Calculate net pay and mpf
    mpf_employer, mpf_employee, net_pay = 0, 0, 0
    past = (period_end - employee.join_date).days + 1  # Past days from join
    if past < 60:  # less than 3 months no mpf
        net_pay = salary
    elif 60 <= past < 90:  # 3rd month
        payments = Payment.objects.all().filter(employee=employee,
                                                period_end__lte=period_start)
        # Employer MPF cumulative
        for p in payments:
            if p.net_pay > 30000:
                mpf_employer += 1500
            else:
                mpf_employer += p.net_pay * 0.05

        if salary > 30000:
            mpf_employee = 1500
            mpf_employer += 1500
        elif 7100 <= salary <= 30000:
            mpf_employee = salary * 0.05
            mpf_employer += salary * 0.05
        else:
            mpf_employer += salary * 0.05

    else:  # 4th month onwards
        if salary > 30000:
            mpf_employee = 1500
            mpf_employer = 1500
        elif 7100 <= salary <= 30000:
            mpf_employee = salary * 0.05
            mpf_employer = salary * 0.05
        else:
            mpf_employer = salary * 0.05

    total_payments = employee.salary
    total_deductions = mpf_employee + no_pay_leave
    net_pay = total_payments - total_deductions

    # Annual Leave
    year_end = datetime.date(period_end.year, 12, 31)
    workdays_after_end = (year_end - period_end).days
    days_of_year = 0
    if calendar.isleap(period_end.year):
        days_of_year = 366
    else:
        days_of_year = 365
    leaves_after_end = round(workdays_after_end / days_of_year * 15 * 2) / 2
    leaves_unused = employee.annual_leave - leaves_after_end

    return {'basic_salary': employee.salary, 'mpf_employer': mpf_employer,
            'mpf_employee': mpf_employee, 'net_pay': net_pay, 'no_pay_leave': no_pay_leave,
            'total_payments': total_payments, 'total_deductions': total_deductions,
            'join_date': employee.join_date, 'leaves_unused': leaves_unused}
