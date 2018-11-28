from django.db import models
import uuid
from django.urls import reverse

# Create your models here.
class Employee(models.Model):
    staff_no = models.CharField(max_length = 10, default = str(uuid.uuid4().int)[:6], unique = True, primary_key=True, blank=True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    start_date = models.DateField()
    salary = models.FloatField(default = 20000)
    address = models.CharField(max_length = 100, default = 'Kowloon, Hong Kong')
    phone_no = models.CharField(max_length = 20, default = '+852-65564053')
    annual_leave = models.DecimalField(max_digits = 3, decimal_places = 0, default = 12)
    email = models.EmailField(default = 'test@81.com')
    bank_acc = models.CharField(max_length = 100, default = '123-456-778')
    department = models.CharField(max_length = 100, default = '-')

    class Meta:
        ordering = ['-last_name']

    def get_absolute_url(self):
        return reverse('personal_details:detail', kwargs={'pk': self.pk})

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
