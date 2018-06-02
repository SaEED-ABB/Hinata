from . import jalali
from django.utils.timezone import localtime


def get_solar_date(datetime):
    local_datetime = localtime(datetime)
    date = jalali.Gregorian(local_datetime.date())
    time = local_datetime.time()
    context = {
        'year': date.persian_year,
        'month': date.persian_month,
        'day': date.persian_day,
        'hour': time.hour,
        'minute': time.minute,
        'second': time.second
    }
    return context