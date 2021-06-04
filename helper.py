"""Helper methods"""

import datetime


def scheduled_time_today(hour, min):
    """
    :return: scheduled timestamp
    """
    today = datetime.date.today()
    # tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    scheduled_time = datetime.time(hour=hour, minute=min)
    schedule_timestamp = datetime.datetime.combine(today, scheduled_time).strftime('%s')
    print('schedule_timestamp', schedule_timestamp)
    return schedule_timestamp


def time_date_now():
    """
    :return: datetime, timestemp of time on the moment
    """
    datetime_now = datetime.datetime.now()
    timestamp_now = int(datetime_now.timestamp())
    return datetime_now, timestamp_now


def task_scheduler(task):
    """
    Run task by system scheduler
    :param task: method to run by scheduler
    """
    import schedule
    import time

    schedule.every().friday.at("12:00").do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)