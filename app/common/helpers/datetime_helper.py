from datetime import date, datetime, time, timedelta
from pytz import timezone

import pytz
from django.utils import timezone

IST_TIMEZONE = pytz.timezone("Asia/Kolkata")


def get_start_date_end_date_in_datetime_from_epoch_in_seconds(
    start_date_epoch, end_date_epoch, reset_time=True
):
    start_date, end_date = None, None
    if start_date_epoch:
        start_date = datetime.fromtimestamp(int(start_date_epoch))
        if reset_time:
            start_date = start_date.replace(hour=0, minute=0, second=0)
    if end_date_epoch:
        end_date = datetime.fromtimestamp(int(end_date_epoch))
        if reset_time:
            end_date = end_date.replace(hour=23, minute=59, second=59)
    return start_date, end_date


def get_start_date_end_date_in_datetime(start_date_epoch, end_date_epoch):
    start_date, end_date = None, None
    if start_date_epoch:
        if len(str(start_date_epoch)) <= 11:
            return get_start_date_end_date_in_datetime_from_epoch_in_seconds(start_date_epoch, end_date_epoch)

        start_date = datetime.fromtimestamp(int(start_date_epoch) / 1000) + timedelta(hours = 5.5)
        start_date = start_date.replace(hour = 0, minute = 0, second = 0)
    if end_date_epoch:
        if len(str(start_date_epoch)) <= 11:
            return get_start_date_end_date_in_datetime_from_epoch_in_seconds(start_date_epoch, end_date_epoch)

        end_date = datetime.fromtimestamp(int(end_date_epoch) / 1000) + timedelta(hours = 5.5)
        end_date = end_date.replace(hour = 23, minute = 59, second = 59)
    return start_date, end_date