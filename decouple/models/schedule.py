import datetime
from typing import Protocol

from models.period import Period, first_working_day, last_working_day


class Schedule(Protocol):
    discrim = "BASE"

    def get_occurences_in_period(self, period: Period) -> list[datetime.date]:
        raise NotImplementedError("Not Implemented")

    @classmethod
    def from_dict(cls, input_dict):
        # 1. find subclass with correct discrim
        for sub in cls.__subclasses__():
            if hasattr(sub, "discrim"):
                if sub.discrim == input_dict.get("type", None):
                    return sub(**input_dict["args"])

    def to_dict(self):
        output = {"type": self.discrim, "args": self.__dict__}
        return output


class AnchoredExpenseSchedule(Schedule):
    discrim = "anchored"

    def __init__(self, anchor: int) -> None:
        self.anchor = anchor

    def get_occurences_in_period(self, period: Period) -> list[datetime.date]:
        occurences = []
        number_of_days_in_window = period.days_in_period()
        for i in range(number_of_days_in_window):
            dtc = period.start + datetime.timedelta(days=i + 1)
            if dtc.day == self.anchor:
                occurences.append(dtc)

        print(f"Event occures {len(occurences)} times")
        return occurences


class FirstLastWorkingDayMonthlyExpenseSchedule(Schedule):
    discrim = "first_last_working"

    def __init__(self, anchor):
        super().__init__()
        if anchor == "f":
            self.checker = first_working_day
        elif anchor == "l":
            self.checker = last_working_day
        else:
            raise ValueError(
                f"Must choose first or last working day. Something else was given: {anchor}"
            )

    def get_occurences_in_period(self, period: Period) -> list[datetime.date]:
        occurences = []
        number_of_days_in_window = period.days_in_period()
        for i in range(number_of_days_in_window):
            dtc = period.start + datetime.timedelta(days=i + 1)
            if dtc == self.checker(dtc):
                occurences.append(dtc)
        print(f"Event occures {len(occurences)} times")
        return occurences


class WeeklyExpenseSchedule(Schedule):
    discrim = "weekly"

    def __init__(self, weekday):
        super().__init__(self)
        self.weekday = weekday

    def get_occurences_in_period(self, period):
        occurences = []
        number_of_days_in_period = period.days_in_period()
        for i in range(number_of_days_in_period):
            dtc = period.start + datetime.timedelta(days=i + 1)
            if dtc.weekday == self.weekday:
                occurences.append(dtc)
        return occurences


class ASched(Schedule):
    def __init__(self, anchor: int, title: str):
        self.anchor = anchor
        self.title = title

    def __repr__(self):
        return f"ASchedule {self.title} on anchor {self.anchor}"


class BSched(Schedule):
    def __init__(self, day: int, title: str):
        self.day = day
        self.title = title

    def __repr__(self):
        return f"BSchedule {self.title} on day: {self.day}"
