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
    staff_id = models.CharField(max_length=10,
                                default=generate_random_id,
                                unique=True,
                                verbose_name='Employee ID')
    nick_name = models.CharField(
        blank=True, max_length=30, verbose_name='Nick Name')
    last_date = models.DateField(
        null=True, blank=True, verbose_name='Last Date')

    address = models.CharField(max_length=150,
                               default='Unit 801-802, 8/F C-Bons International Centre, 108 Wai Yip Street, Kwun Tong, Kowloon, Hong Kong', blank=True)
    mobile = models.CharField(max_length=20,
                              default='+852-29009999', blank=True)

    department = models.CharField(max_length=100,
                                  default='-', blank=True)
    title = models.CharField(max_length=10, default='-', blank=True)

    annual_leave = models.FloatField(verbose_name='Annual Leave')

    bank = models.CharField(
        max_length=50, choices=choices.BANK_LIST, default='024', blank=True)
    bank_acc = models.CharField(max_length=100,
                                default='123-456-778', blank=True, verbose_name='Bank Account')
    salary = models.FloatField(null=True, blank=True)

    slug = models.SlugField(blank=True)

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
