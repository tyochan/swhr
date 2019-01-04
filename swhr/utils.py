import datetime


def leave_spend_days(start_date, end_date):
    # Calculate spend days
    spend = (l.end_date - start_date).days + 1
    # Weekends
    temp = start_date
    while temp < l.end_date + datetime.timedelta(days=1):
        if temp.isoweekday() == 6 or temp.isoweekday() == 7:
            spend -= 1
        temp += datetime.timedelta(days=1)

    # Holidays
    for h in constant.HOLIDAYS:
        date = datetime.datetime.strptime(h, '%Y-%m-%d').date()
        if start_date < date < end_date:
            spend -= 1

    return spend
