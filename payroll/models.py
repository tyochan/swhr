from django.db import models
from personal_details.models import Employee
from leave_records.models import Leave

# Create your models here.


class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
