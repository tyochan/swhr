# Models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify

# Utils
import uuid
from . import choices
from django.urls import reverse


def generate_random_id():
    random_id = str(uuid.uuid4().int)[:6]
    while User.objects.filter(id=random_id).count():
        random_id = str(uuid.uuid4().int)[:6]
    return random_id

# Create your models here.


class User(AbstractUser):
    slug = models.SlugField(blank=True)  # Hidden Info
    # id
    # Basic Info
    # username password first_name last_name
    nick_name = models.CharField(
        blank=True, max_length=30, verbose_name='Nick Name')
    staff_id = models.CharField(max_length=10,
                                default=generate_random_id,
                                unique=True,
                                verbose_name='Employee ID')

    # Identity
    birth_date = models.DateField(null=True, verbose_name='Date of Birth')
    identity_type = models.CharField(
        max_length=10, choices=choices.IDENTITY_TYPE, default='ID', verbose_name='Identity Type')
    identity_no = models.CharField(
        default='1234567', max_length=30, verbose_name='Identity No.')

    # Contact Info
    # email
    mobile = models.CharField(max_length=20,
                              default='+852-29009999', blank=True)
    address = models.CharField(max_length=150,
                               default='Unit 801-802, 8/F C-Bons International Centre, 108 Wai Yip Street, Kwun Tong, Kowloon, Hong Kong', blank=True)
    department = models.CharField(max_length=100,
                                  default='-', blank=True)
    title = models.CharField(max_length=10, default='-')
    title_grade = models.CharField(
        max_length=20, null=True, verbose_name='Title Grade')
    marital_status = models.CharField(max_length=10, default='SI',
                                      choices=choices.MARITAL_STATUS, verbose_name='Marital Status')

    # Pay Info
    annual_leave = models.FloatField(default=0, verbose_name='Annual Leave')
    bank = models.CharField(
        max_length=50, choices=choices.BANK_LIST, default='024', blank=True)
    bank_acc = models.CharField(max_length=100,
                                default='123-456-778', blank=True, verbose_name='Bank Account')
    salary = models.FloatField(default=0)
    salary_grade = models.CharField(
        max_length=20, null=True, verbose_name='Salary Grade')

    # Emergency Contact
    emergency_contact_name = models.CharField(
        blank=True, null=True, max_length=30, verbose_name='Name')
    emergency_contact_number = models.CharField(blank=True, null=True, max_length=20,
                                                default='+852-29009999', verbose_name='Number')
    emergency_contact_relationship = models.CharField(
        blank=True, null=True, max_length=30, verbose_name='Relationship')

    # Admin Info
    # last_login is_superuser is_staff is_active date_joined groups user_permissions
    last_date = models.DateField(
        null=True, blank=True, verbose_name='Last Date')

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('personal_details:index')  # , kwargs={'pk': self.pk}

    def __str__(self):
        return '%s %s %s' % (self.staff_id, self.last_name, self.first_name)

    def get_name(self):
        return '%s %s' % (self.last_name, self.first_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.staff_id)
        super(User, self).save(*args, **kwargs)


class SalaryRecord(models.Model):
    date_changed = models.DateField(verbose_name='Date')
    amount = models.FloatField()
    grade = models.CharField(max_length=10, verbose_name='Salary Grade')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (date_changed, amount)


class TitleRecord(models.Model):
    date_changed = models.DateField(verbose_name='Date')
    #department = models.CharField(verbose_name='Department')
    name = models.CharField(max_length=30, verbose_name='Title')
    grade = models.CharField(max_length=20, verbose_name='Title Grade')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (date_changed, name, grade)


class AcademicRecord(models.Model):
    date_start = models.DateField(verbose_name='From Date')
    date_end = models.DateField(verbose_name='End Date')
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' % (date_start, date_end, name)


class Spouse(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    identity_type = models.CharField(
        max_length=10, choices=choices.IDENTITY_TYPE, default='ID', verbose_name='Identity Type')
    identity_no = models.CharField(max_length=30, verbose_name='Identity No.')
