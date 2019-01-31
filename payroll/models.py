# Models
from django.db import models
from personal_details.models import User

# Utils
from . import choices


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    method = models.CharField(
        choices=choices.PAYMENT_METHOD,
        default=choices.PAYMENT_METHOD[0][0],
        max_length=10,
    )
    period_start = models.DateField(
        verbose_name='Period Start'
    )
    period_end = models.DateField(
        verbose_name='Period End'
    )
    pay_date = models.DateField(
        verbose_name='Pay Date'
    )

    # Payments
    basic_salary = models.FloatField(
        verbose_name='Basic Salary'
    )
    allowance = models.FloatField(
        blank=True,
        default=0,
    )
    other_payments = models.FloatField(
        blank=True,
        default=0,
        verbose_name='Others'
    )
    total_payments = models.FloatField(
        verbose_name='Total'
    )

    # Deductions
    np_leave = models.FloatField(
        default=0,
        verbose_name='No Pay Leaves'
    )
    other_deductions = models.FloatField(
        blank=True,
        default=0,
        verbose_name='Others'
    )
    total_deductions = models.FloatField(
        verbose_name='Total'
    )

    # MPF
    mpf_employer = models.FloatField(
        verbose_name='MPF Employer Contribution'
    )
    mpf_employee = models.FloatField(
        verbose_name='MPF Employee Contribution'
    )

    net_pay = models.FloatField(
        verbose_name='Net Pay'
    )
    status = models.CharField(
        choices=choices.STATUS_CHOICES,
        default=choices.STATUS_CHOICES[0][0],
        max_length=10,
    )

    is_last = models.BooleanField(
        blank=True,
        default=False,
    )
    unused_leave_days = models.FloatField(
        blank=True,
        default=0,
        verbose_name='Unused Leaves'
    )
    unused_leave_pay = models.FloatField(
        blank=True,
        default=0,
        verbose_name='Pay For Unused Leaves'
    )

    class meta:
        ordering = ['-period_start']

    def __str__(self):
        return f'{self.user}: {self.period_start} to {self.period_end} of ${self.net_pay}'

    @property
    def third_month(self):
        return 60 <= (self.period_end - self.user.date_joined.date()).days + 1 < 90

    @property
    def start_late(self):
        return self.period_start < self.user.date_joined.replace(tzinfo=None).date()
