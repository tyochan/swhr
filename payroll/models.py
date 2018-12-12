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
    mpf_employer = models.FloatField()
    mpf_employee = models.FloatField()
    net_pay = models.FloatField()
