from django.db import models
import uuid
import datetime
from django.urls import reverse
from django.utils import timezone

default_address = 'Unit 801-802, 8/F C-Bons International Centre, 108 Wai Yip Street, Kwun Tong, Kowloon, Hong Kong'
default_date = timezone.now()
default_salary = 20000
default_phone_no = '+852-65564053'
default_annual_leave = 12
default_email = 'test@81.com'
default_bank_acc = '123-456-778'
default_department = '-'


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
    start_date = models.DateField(default=default_date, blank=True)
    salary = models.FloatField(default=default_salary, blank=True)
    address = models.CharField(max_length=150,
                               default=default_address, blank=True)
    phone_no = models.CharField(max_length=20,
                                default=default_phone_no, blank=True)
    annual_leave = models.DecimalField(max_digits=3,
                                       decimal_places=0,
                                       default=default_annual_leave, blank=True)
    email = models.EmailField(default=default_email, blank=True)
    bank_acc = models.CharField(max_length=100,
                                default=default_bank_acc, blank=True)
    department = models.CharField(max_length=100,
                                  default=default_department, blank=True)

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('personal_details:index')  # , kwargs={'pk': self.pk}

    # def randomID():
    #     random_number = User.objects.make_random_password(length=6, allowed_chars='0123456789')
    #     while User.objects.filter(staff_no = random_number):
    #         random_number = User.objects.make_random_password(length=6, allowed_chars='0123456789')
    #     return random_number

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    # c_family_name = models.CharField(max_length = 30)
    # c_name = models.CharField(max_length = 30)
    # end_date = models.DateField()
    # existing = models.BooleanField()
    # job_title = models.CharField(max_length = 100)
    # office_phone_no = models.CharField(max_length = 20)
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
