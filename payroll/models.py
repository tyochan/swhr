from django.db import models
from personal_details.models import Employee
from leave_records.models import Leave
from . import choices

# Create your models here.


class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    method = models.CharField(
        max_length=10, choices=choices.PAYMENT_METHOD, default='Cheque')
    period_start = models.DateField()
    period_end = models.DateField()
    pay_date = models.DateField()

    # Payments
    basic_salary = models.FloatField()
    allowance = models.FloatField(blank=True, default=0)
    other_payments = models.FloatField(blank=True, default=0)
    total_payments = models.FloatField()

    # Deductions
    np_leave = models.FloatField()
    other_deductions = models.FloatField(blank=True, default=0)
    total_deductions = models.FloatField()

    # MPF
    mpf_employer = models.FloatField()
    mpf_employee = models.FloatField()

    net_pay = models.FloatField()
    # status = models.CharField(
    #     max_length=10, choices=choices.STATUS_CHOICES, default='PD', blank=True)

    class meta:
        ordering = ['-period_start']

    def __str__(self):
        return '%s to %s, %s, $%s' % (self.period_start, self.period_end, self.employee, self.net_pay)

    @property
    def third_month(self):
        return 60 <= (self.period_end - self.employee.join_date).days + 1 < 90

    @property
    def start_late(self):
        return self.period_start < self.employee.join_date
