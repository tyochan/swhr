# Models
from django.db import models
from personal_details.models import User

# Utils
from . import choices
from django.urls import reverse

# Create your models here.


class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_date = models.DateField(verbose_name='Start Date')
    end_date = models.DateField(verbose_name='End Date')
    day_type = models.CharField(
        max_length=20, choices=choices.LEAVE_DAY_TYPE, default='FD', blank=True, verbose_name='Day Type')
    spend = models.FloatField(verbose_name='Leave Spend')

    type = models.CharField(
        max_length=30, choices=choices.LEAVE_TYPE, default='AL', verbose_name='Leave Type')
    remarks = models.CharField(max_length=500, blank=True, null=True)

    status = models.CharField(
        max_length=10, choices=choices.STATUS_CHOICES, default='PD', blank=True)

    # class Meta:
    #      ordering = ['status']

    def get_absolute_url(self):
        return reverse('leave_records:index')

    def __str__(self):
        return '%s %s: %s %s from %s to %s as %s days' % (self.user.last_name, self.user.first_name,
                                                          self.get_status_display(), self.get_type_display(),
                                                          self.start_date.strftime('%Y/%m/%d'), self.end_date.strftime('%Y/%m/%d'), self.spend)
