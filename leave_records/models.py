# Models
from django.db import models
from personal_details.models import User

# Utils
from . import choices
from django.urls import reverse

# Create your models here.


class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_date = models.DateField(
        verbose_name='Start Date'
    )
    end_date = models.DateField(
        verbose_name='End Date'
    )
    day_type = models.CharField(
        choices=choices.LEAVE_DAY_TYPE,
        default=choices.LEAVE_DAY_TYPE[0][0],
        max_length=20,
        verbose_name='Day Type'
    )
    spend = models.FloatField(
        verbose_name='Leave Spend'
    )

    type = models.CharField(
        choices=choices.LEAVE_TYPE,
        default=choices.LEAVE_TYPE[0][0],
        max_length=5,
        verbose_name='Leave Type'
    )
    remarks = models.CharField(
        blank=True,
        max_length=500,
        null=True,
    )

    status = models.CharField(
        blank=True,
        choices=choices.STATUS_CHOICES,
        default=choices.STATUS_CHOICES[0][0],
        max_length=10,
    )

    # class Meta:
    #      ordering = ['status']

    def get_absolute_url(self):
        return reverse('leave_records:index')

    def __str__(self):
        return f'{self.user.get_name()}: {self.get_status_display()} {self.get_type_display()} from {self.start_date.strftime("%Y/%m/%d")} to {self.end_date.strftime("%Y/%m/%d")} as {self.spend} days'
