from django.db import models
from personal_details.models import Employee
from django.utils import timezone
from django.urls import reverse
import datetime
import uuid
from . import choices

default_status = "Pending"


def generate_random_id():
    random_id = str(uuid.uuid4().int)[:10]
    while Leave.objects.filter(serial_no=random_id).count():
        random_id = str(uuid.uuid4().int)[:10]
    return random_id

# Create your models here.


class Leave(models.Model):
    serial_no = models.CharField(max_length=10,
                                 default=generate_random_id,
                                 unique=True,
                                 primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    spend = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=choices.STATUS_CHOICES, default='PD')
    remarks = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(
        max_length=30, choices=choices.LEAVE_TYPE, default='AL')

    # class Meta:
    # ordering = ['start_date']

    def get_absolute_url(self):
        return reverse('leave_records:index')

    def __str__(self):
        return self.employee.first_name + ' ' + self.employee.last_name + ' ' + self.start_date.strftime('%Y/%m/%d') + ' to ' + self.end_date.strftime('%Y/%m/%d')
