# Models
from django.db import models
from personal_details.models import Employee

# Utils
from . import choices
from django.urls import reverse

# Create your models here.


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    spend = models.FloatField()
    status = models.CharField(
        max_length=10, choices=choices.STATUS_CHOICES, default='PD', blank=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(
        max_length=30, choices=choices.LEAVE_TYPE, default='AL')
    day_type = models.CharField(
        max_length=10, choices=choices.LEAVE_DAY_TYPE, default='FD', blank=True)

    # class Meta:
    #      ordering = ['status']

    def get_absolute_url(self):
        return reverse('leave_records:index')

    def __str__(self):
        return '%s %s: %s %s from %s to %s as %s days' % (self.employee.last_name, self.employee.first_name,
                                                          self.get_status_display(), self.get_type_display(),
                                                          self.start_date.strftime('%Y/%m/%d'), self.end_date.strftime('%Y/%m/%d'), self.spend)
