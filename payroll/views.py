from django.urls import reverse_lazy
from django.views import generic
from .models import Payment
from personal_details.models import Employee
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms
from django.http import HttpResponseRedirect, JsonResponse
from django_ajax.decorators import ajax
import datetime
import calendar

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'payroll.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.all()


class PaymentCreateView(generic.CreateView):
    form_class = forms.PaymentCreateForm
    model = Payment
    template_name = 'form_payment.html'
    success_url = reverse_lazy('payroll:index')


@ajax
def getBasicSalary(request):
    employee = Employee.objects.get(staff_no=request.GET['staff_no'])
    salary = employee.salary
    past = datetime.date.today() - employee.join_date
    mpf_employer = 0
    mpf_employee = 0
    net_pay = 0

    # If third month
    if past.days > 60 and past.days < 90:
        day, num_days = calendar.monthrange(
            employee.join_date.year, employee.join_date.month)
        # Calculate first month mpf for employer
        ratio = (num_days - employee.join_date.day + 1) / num_days
        print(ratio)
        if salary > 30000:
            mpf_employer = 1500 * ratio
        else:  # 5%
            mpf_employer = salary * 0.05 * ratio
        print(mpf_employer)

    return {'basic_salary': salary, 'mpf_employer': mpf_employer, 'mpf_employee': mpf_employee, 'net_pay': net_pay}
