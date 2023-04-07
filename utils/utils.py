import datetime
import jdatetime


def get_jdatetime():
    now = datetime.datetime.now()

    # Convert the current date and time to Persian calendar
    persian_date = jdatetime.date.fromgregorian(date=now)

    # Get the current time in 24-hour format
    time = now.strftime("%H:%M")
    persian_date = persian_date.strftime("%Y/%m/%d")
    persian_time = time
    jdate_time = [persian_date, persian_time]
    return jdate_time
