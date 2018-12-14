from django.db import models
import uuid
import datetime
from django.urls import reverse
from django.utils import timezone
from . import choices

default_address = 'Unit 801-802, 8/F C-Bons International Centre, 108 Wai Yip Street, Kwun Tong, Kowloon, Hong Kong'
default_date = timezone.now()
default_salary = 20000
default_phone_no = '+852-12345678'
default_annual_leave = 15
default_email = 'test@81.com'
default_bank = '024'
default_bank_acc = '123-456-778'
default_department = '-'
default_title = '-'


def generate_random_id():
    random_id = str(uuid.uuid4().int)[:6]
    while Employee.objects.filter(staff_no=random_id).count():
        random_id = str(uuid.uuid4().int)[:6]
    return random_id

# Create your models here.


class Employee(models.Model):
    staff_no = models.CharField(max_length=10,
                                default=generate_random_id,
                                unique=True,
                                primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    join_date = models.DateField(default=timezone.now, blank=True)
    salary = models.FloatField(default=default_salary, blank=True)
    address = models.CharField(max_length=150,
                               default=default_address, blank=True)
    phone_no = models.CharField(max_length=20,
                                default=default_phone_no, blank=True)
    annual_leave = models.FloatField(default=default_annual_leave, blank=True)
    email = models.EmailField(default=default_email, blank=True)
    bank = models.CharField(
        max_length=50, choices=choices.BANK_LIST, default=default_bank)
    bank_acc = models.CharField(max_length=100,
                                default=default_bank_acc, blank=True)
    department = models.CharField(max_length=100,
                                  default=default_department, blank=True)
    title = models.CharField(max_length=10, default=default_title, blank=True)
    active = models.BooleanField(default=True)
    leave_date = models.DateField(null=True, blank=True)
    # office_phone_no = models.CharField(max_length = 20)

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('personal_details:index')  # , kwargs={'pk': self.pk}

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    # c_family_name = models.CharField(max_length = 30)
    # c_name = models.CharField(max_length = 30)

    # nationality = models.CharField(max_length = 30)
    # birth_date = models.DateField()
    # marital_status = models.CharField(max_length = 20)
    # supervisor = models.CharField()

# class Spouse(models.Model):
    # employee_id = models.ForeignKey(Employee, on_delete = models.CASCADE)
    # first_name = models.CharField(max_length = 30)
    # middle_name = models.CharField(max_length = 30)
    # last_name = models.CharField(max_length = 30)
    # phone_no = models.CharField(max_length = 20)
