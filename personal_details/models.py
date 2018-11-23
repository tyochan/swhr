from django.db import models

# Create your models here.
class Employee(models.Model):
    id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length = 30)
    middle_name = models.CharField(max_length = 30, blank = True)
    last_name = models.CharField(max_length = 30)
    start_date = models.DateField()
    salary = models.FloatField()
    address = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 20)
    annual_leave = models.DecimalField(max_digits = 3, decimal_places = 0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    # c_family_name = models.CharField(max_length = 30)
    # c_name = models.CharField(max_length = 30)
    # staff_no = models.CharField(max_length = 100)
    # email = models.EmailField()
    # end_date = models.DateField()
    # existing = models.BooleanField()
    # bank_acc = models.CharField(max_length = 100)
    # department = models.CharField(max_length = 100)
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
