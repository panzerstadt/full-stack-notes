import datetime
import math

def countdown(due_date='2000/01/01', days_only=False):
    """
    :param due_date: year/month/day/hour   hour is optional
    :return: string denoting time left
    """
    # create countdown timer
    future = [int(s) for s in due_date.split('/')]
    f = future
    future = datetime.datetime(year=f[0], month=f[1], day=f[2])
    current = datetime.datetime.now()

    time_left = future - current
    time_left = time_left.days

    if days_only:
        print('time left:', time_left, 'days')
        return time_left

    def year(days):
        if days % 365 != days:
            return int(days / 365)
        else: return 0

    def month(days):
        years = year(days)
        if years >= 1:
            days = days - (years * 365)
        if days % 30 != days:
            return int(days / 30)
        else: return 0

    def day(days):
        months = month(days)
        years = year(days)
        if months >= 1:
            days = days - (years * 365) - (months * 30)
        return days

    t = time_left
    return '{0}yr {1}mth {2}dy left.'.format(year(t), month(t), day(t))


print(countdown('2019/05/22'))