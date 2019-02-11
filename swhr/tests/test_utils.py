from django.test import TestCase, Client, RequestFactory
from personal_details.models import User, SalaryTitleRecord, AcademicRecord, EmploymentHistory
from personal_details.forms import AcademicRecordForm, AcademicRecordFormsetHelper
from django.contrib.auth.models import AnonymousUser
from swhr.views import CustomLoginView, CustomPasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from swhr import utils, constant
from crispy_forms.layout import LayoutObject
from django.template.loader import render_to_string
from django.forms.models import inlineformset_factory

import datetime


class UtilsTest(TestCase):
    # def setUp(self):
    #     test_user1 = User.objects.create_superuser(
    #         username='testuser1', password='1X<ISRUkw+tuK', email='admin@81.com')
    #     test_user2 = User.objects.create_user(
    #         username='testuser2', password='1X<ISRUkw+tuK')
    #     test_user3 = User.objects.create_user(
    #         username='testuser3', password='1X<ISRUkw+tuK')
    #
    #     test_user1.save()
    #     test_user2.save()
    #     test_user3.save()

    def test_formset_layout_object(self):
        AcademicRecordInlineFormset = inlineformset_factory(
            User, AcademicRecord,
            form=AcademicRecordForm,
            can_delete=False,
            extra=1,
        )
        formset = utils.Formset(
            AcademicRecordInlineFormset, AcademicRecordFormsetHelper())
        self.assertEqual(utils.Formset.template, formset.template)

    def test_get_holidays(self):
        self.assertEqual(utils.get_holidays(), constant.HOLIDAYS)

    def test_period_spend_days_1(self):
        start_date = datetime.datetime.strptime('2019-2-1', '%Y-%m-%d')
        end_date = datetime.datetime.strptime('2019-2-28', '%Y-%m-%d')
        spend = utils.period_spend_days(start_date, end_date)
        self.assertEqual(spend, 17)

    def test_period_spend_days_2(self):
        start_date = datetime.datetime.strptime('2019-3-1', '%Y-%m-%d')
        end_date = datetime.datetime.strptime('2019-3-7', '%Y-%m-%d')
        spend = utils.period_spend_days(start_date, end_date)
        self.assertEqual(spend, 5)

    def test_period_spend_days_3(self):
        start_date = datetime.datetime.strptime('2019-4-30', '%Y-%m-%d')
        end_date = datetime.datetime.strptime('2019-5-8', '%Y-%m-%d')
        spend = utils.period_spend_days(start_date, end_date)
        self.assertEqual(spend, 6)

    def test_annual_leave_to_year_end_1(self):
        start_date = datetime.datetime.strptime(
            '2019-12-13', '%Y-%m-%d').date()
        annual_leave = utils.annual_leave_to_year_end(start_date)
        self.assertEqual(annual_leave, 1)

    def test_annual_leave_to_year_end_2(self):
        start_date = datetime.datetime.strptime(
            '2019-12-1', '%Y-%m-%d').date()
        annual_leave = utils.annual_leave_to_year_end(start_date)
        self.assertEqual(annual_leave, 1.5)

    def test_annual_leave_to_year_end_3(self):
        start_date = datetime.datetime.strptime(
            '2019-12-2', '%Y-%m-%d').date()
        annual_leave = utils.annual_leave_to_year_end(start_date)
        self.assertEqual(annual_leave, 1)
