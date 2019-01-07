import calendar
import datetime
from . import constant


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
    workdays = (end_date - start_date.date()).days + 1
    days_of_year = 366 if calendar.isleap(end_date.year) else 365
    annual_leave = round((workdays / days_of_year * 15) * 2) / 2
    return annual_leave
