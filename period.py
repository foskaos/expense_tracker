import datetime


def month_cycle(start, n):
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # fixme: not sure about subtracting 1 from start for new index.
    new_index = ((start - 1) + n) % 12
    return months[new_index]


def increment_date_by_months(date: datetime.date, increment: int) -> datetime.date:
    new_month = month_cycle(date.month, increment)

    # check if we are moving years
    if (date.month + increment) >= 13:
        # FIXME: subtracting 1 below seems to fix additions of years, not sure why though
        yrs = (date.month + increment - 1) // 12
    else:
        yrs = 0

    try:
        new_date = date.replace(month=new_month, year=yrs + date.year)
        last_day_error = False
    except ValueError as e:
        # go to last day of next month and then subtract one day
        new_date = (
            datetime.datetime(year=date.year + yrs, month=new_month + 1, day=1)
            - datetime.timedelta(days=1)
        ).date()
        last_day_error = True

    print(
        f"Start Date: {date}, New Date: {new_date}, Increment: {increment}. {'last day error' if last_day_error else ''}"
    )
    return new_date


def is_weekday(date: datetime.date)->bool:

    if date.weekday() in [5,6]:
        return False
    return True


def last_working_day(date: datetime.date)->datetime.date:
    """finds the last working day of the month for the month of the given date"""
    day_to_check = increment_date_by_months(date, 1).replace(day = 1) - datetime.timedelta(days=1)

    while True:
        if is_weekday(day_to_check):
            break 
        day_to_check = day_to_check - datetime.timedelta(days=1)

    return day_to_check        

def increment_date_by_weeks(date: datetime.date, weeks: int)->datetime.date:
    return date + datetime.timedelta(days=7*weeks)



class Period:
    def __init__(self, start: datetime.date, end: datetime.date = None, interval: str = None, number: int = None):
        self.start = start
        if end:
            self.end = end
        elif interval and number:
            self.interval = interval
            self.number = number
            self.end = self._get_period_end()
        else:
            raise Exception('Either end date OR interval AND number to be provided')

    def _get_period_end(self):
        match self.interval:
            case 'M':
                end = increment_date_by_months(self.start, self.number)
            case 'W':
                end = increment_date_by_weeks(self.start, self.number)
            case _:
                raise NotImplementedError('Interval not recognized.')
        return end

    def make_period_list(self):
        match self.interval:
            case 'M':
                incrementor = increment_date_by_months
            case 'W':
                incrementor = increment_date_by_weeks
            case _:
                raise NotImplementedError('No valid incrementor defined')

        plist = []
        start = self.start
        end = None
        while True:
            end = incrementor(start, 1)
            if end <= self.end:
                plist.append((start,end-datetime.timedelta(days=1)))
                start = end
                end = None
            else:
                if start >= self.end:
                    break
                plist.append((start,self.end-datetime.timedelat(days=1)))
                break

        return plist

    def days_in_period(self):
        return (self.end - self.start).days
    
    def months_in_period(self):
        """returns the unique months in a period"""
        mip = []
        month = self.start.replace(day=1)

        while True:
            if month in mip:
                continue
            mip.append(month)
            nm = increment_date_by_months(month,1)

            if nm > self.end:

                break
            month = nm

        return mip
