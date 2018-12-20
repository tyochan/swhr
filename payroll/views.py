from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Payment
from leave_records.models import Leave
from personal_details.models import Employee
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django_ajax.decorators import ajax
import datetime
import calendar
from django.db.models import Q
from swhr import strings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_weasyprint import WeasyTemplateResponseMixin
from weasyprint import HTML
import tempfile

# Create your views here.


class IndexView(ListView):
    template_name = 'payroll.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.all().order_by('period_start')


class PaymentCreateView(CreateView):
    form_class = forms.PaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')


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


@ajax
def calculateSalary(request):
    employee = Employee.objects.get(staff_no=request.GET['staff_no'])

    print('Salary: (Period End Date - Period Join/Start Date - Leave Spend + 1) / Period Max Days * Basic Salary')
    # Split and parse string date to int list
    period_start = [int(x) for x in request.GET['period_start'].split("-")]
    period_end = [int(x) for x in request.GET['period_end'].split("-")]
    period_start = datetime.date(
        period_start[0], period_start[1], period_start[2])
    period_end = datetime.date(period_end[0], period_end[1], period_end[2])
    print('Period: %s - %s' % (period_start, period_end))

    # Max days this pay period
    period_max = (period_end - period_start).days + 1
    print('Period Max Days = %s' % period_max)
    # First month
    if (period_end - employee.join_date).days < 32:
        period_work = (period_end - employee.join_date).days + 1
    else:
        period_work = period_max
    print('Expected Period Work Days (with holidays and weekends) = %s' %
          period_work)

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
        print('Leave: %s - %s, spend %s days' %
              (l.start_date, l.end_date, spend))

    print('Actual Period Work Days (with holidays and weekends) = %s' % period_work)
    ratio = period_work / period_max
    salary = employee.salary * ratio
    no_pay_leave = employee.salary * (period_max - period_work) / period_max
    print('Salary: %s * %s = %s' % (employee.salary, ratio, salary))

    # Calculate net pay and mpf
    mpf_employer, mpf_employee, net_pay = 0, 0, 0
    past = (period_end - employee.join_date).days + 1  # Past days from join
    print('Days passed from join date: %s' % past)
    if past < 60:  # less than 3 months no mpf
        print('Join Date: %s' % employee.join_date)
        net_pay = salary
    elif 60 <= past < 90:  # 3rd month
        print('3rd month payment')
        payments = Payment.objects.all().filter(employee=employee,
                                                period_end__lte=period_start)
        # Employer MPF cumulative
        for p in payments:
            if p.net_pay > 30000:
                mpf_employer += 1500
            else:
                mpf_employer += p.net_pay * 0.05
                print(mpf_employer)

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
