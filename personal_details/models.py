# Models
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utils
import uuid
from . import choices
from django.urls import reverse
import django.utils.timezone


def generate_random_id():
    random_id = str(uuid.uuid4().int)[:6]
    while User.objects.filter(id=random_id).count():
        random_id = str(uuid.uuid4().int)[:6]  # pragma: no cover
    return random_id

# Create your models here.


class User(AbstractUser):
    slug = models.SlugField(
        blank=True
    )  # Hidden Info
    # id
    # Basic Info
    # username password first_name last_name
    nick_name = models.CharField(
        blank=True,
        max_length=30,
        null=True,
        verbose_name='Nick Name'
    )
    staff_id = models.CharField(
        default=generate_random_id,
        max_length=10,
        unique=True,
        verbose_name='Employee ID'
    )

    # Identity
    birth_date = models.DateField(
        default=django.utils.timezone.now,
        verbose_name='Date of Birth',
    )
    identity_type = models.CharField(
        choices=choices.IDENTITY_TYPE,
        default=choices.IDENTITY_TYPE[0][0],
        max_length=5,
        verbose_name='Identity Type'
    )
    identity_no = models.CharField(
        max_length=30,
        null=True,
        verbose_name='Identity No'
    )

    # Contact Info
    # email
    mobile = models.CharField(
        max_length=20,
        null=True,
    )
    address = models.CharField(
        max_length=150,
        null=True,
    )
    department = models.CharField(
        choices=choices.DEPARTMENT_LIST,
        default=choices.DEPARTMENT_LIST[-2][0],
        max_length=5,
    )
    title = models.CharField(
        max_length=50,
        null=True,
    )
    grade = models.CharField(
        choices=choices.TITLE_GRADE,
        default=choices.TITLE_GRADE[0][0],
        max_length=5,
    )
    marital_status = models.CharField(
        choices=choices.MARITAL_STATUS,
        default=choices.MARITAL_STATUS[0][0],
        max_length=5,
        verbose_name='Marital Status'
    )

    # Pay Info
    old_annual_leave = models.FloatField(
        blank=True,
        default=0,
        verbose_name='Old Annual Leave'
    )
    annual_leave = models.FloatField(
        default=0,
        verbose_name='Annual Leave'
    )
    bank = models.CharField(
        choices=choices.BANK_LIST,
        default=choices.BANK_LIST[0][0],
        max_length=3,
    )
    bank_acc = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Bank Account'
    )
    salary = models.FloatField(
        default=0,
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(
        max_length=30,
        null=True,
        verbose_name='Emergency Contact Person'
    )
    emergency_contact_number = models.CharField(
        max_length=20,
        null=True,
        verbose_name='Emergency Contact Number'
    )
    emergency_contact_relationship = models.CharField(
        max_length=30,
        null=True,
        verbose_name='Relationship'
    )

    # Admin Info
    # last_login is_superuser is_staff is_active date_joined groups user_permissions
    last_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Last Date'
    )

    class Meta:
        ordering = ['last_name']

    def get_absolute_url(self):
        return reverse('personal_details:index')  # , kwargs={'pk': self.pk}

    def __str__(self):
        return f'{self.staff_id} {self.last_name} {self.first_name}'

    def get_name(self):
        return f'{self.last_name} {self.first_name}'


class AcademicRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_start = models.DateField(
        verbose_name='Start Date'
    )
    date_end = models.DateField(
        verbose_name='End Date'
    )
    institution_name = models.CharField(
        max_length=50,
        verbose_name='Institution Name'
    )
    qualification = models.CharField(
        max_length=100
    )
    year_completed = models.CharField(
        choices=choices.YEAR_LIST,
        default=choices.YEAR_LIST[-1][0],
        max_length=4,
        verbose_name='Year'
    )

    def __str__(self):
        return f'{self.date_start} {self.date_end} {self.institution_name} {self.qualification} {self.year_completed}'


class EmploymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_start = models.DateField(
        verbose_name='Start Date'
    )
    date_end = models.DateField(
        verbose_name='End Date'
    )
    employer_name = models.CharField(
        max_length=50,
        verbose_name='Employer Name'
    )
    position = models.CharField(
        max_length=50,
        verbose_name='Last Position'
    )
    reason = models.CharField(
        max_length=50,
        verbose_name='Reasons for Leaving'
    )

    def __str__(self):
        return f'{self.date_start} to {self.date_end} {self.employer_name} {self.position} {self.reason}'


class SalaryTitleRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_changed = models.DateField(
        verbose_name='Date'
    )
    department = models.CharField(
        choices=choices.DEPARTMENT_LIST,
        max_length=5,
    )
    grade = models.CharField(
        choices=choices.TITLE_GRADE,
        max_length=10,
    )
    salary = models.FloatField()
    title = models.CharField(
        max_length=30,
    )

    def __str__(self):
        return f'{self.date_changed} {self.title} {self.grade} {self.salary}'


class Spouse(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(
        max_length=40,
        null=True,
        verbose_name='Spouse Name'
    )
    identity_type = models.CharField(
        choices=choices.IDENTITY_TYPE,
        default=choices.IDENTITY_TYPE[0][0],
        max_length=10,
        verbose_name='Identity Type'
    )
    identity_no = models.CharField(
        max_length=30,
        null=True,
        verbose_name='Identity No.'
    )

    def __str__(self):
        return f'{self.user} {self.name} {self.identity_type} {self.identity_no}'
