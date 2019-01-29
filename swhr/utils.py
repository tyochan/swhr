import calendar
import datetime
from . import constant
from crispy_forms.layout import LayoutObject
from django.template.loader import render_to_string


class Formset(LayoutObject):
    """
    Renders an entire formset, as though it were a Field.
    Accepts the names (as a string) of formset and helper as they
    are defined in the context

    Examples:
        Formset('contact_formset')
        Formset('contact_formset', 'contact_formset_helper')
    """

    template = "formset.html"

    def __init__(self, formset_context_name, helper_context_name=None,
                 template=None, label=None):

        self.formset_context_name = formset_context_name
        self.helper_context_name = helper_context_name

        # crispy_forms/layout.py:302 requires us to have a fields property
        self.fields = []

        # Overrides class variable with an instance level variable
        if template:
            self.template = template

    def render(self, form, form_style, context, **kwargs):
        formset = context.get(self.formset_context_name)
        helper = context.get(self.helper_context_name)

        # closes form prematurely if this isn't explicitly stated
        if helper:
            helper.form_tag = False
            if not formset.can_delete and ('AR' in self.formset_context_name or 'EH' in self.formset_context_name):
                print('%s not for delete.' % self.formset_context_name)
                # helper.layout[0].pop(-1)
                helper.layout.pop(-2)

        context.update({'formset': formset, 'helper': helper})
        return render_to_string(self.template, context.flatten())


def get_holidays():
    return constant.HOLIDAYS


def period_spend_days(start_date, end_date):
    # Calculate spend days
    spend = (end_date - start_date).days + 1
    # Weekends
    temp = start_date
    while temp < end_date + datetime.timedelta(days=1):
        if temp.isoweekday() == 6 or temp.isoweekday() == 7:
            spend -= 1
        temp += datetime.timedelta(days=1)

    # Holidays
    for h in constant.HOLIDAYS:
        date = datetime.datetime.strptime(h, '%Y-%m-%d')
        if start_date < date < end_date:
            spend -= 1

    return spend


def annual_leave_to_year_end(start_date):
    end_date = datetime.date(start_date.year, 12, 31)
    workdays = (end_date - start_date).days + 1
    days_of_year = 366 if calendar.isleap(end_date.year) else 365
    annual_leave = round((workdays / days_of_year * 15) * 2) / 2
    return annual_leave
