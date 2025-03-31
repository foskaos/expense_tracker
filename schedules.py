from abc import ABC, abstractmethod
import datetime
from period import Period, last_working_day, first_working_day


class ExpenseSchedule(ABC):
    @abstractmethod
    def get_occurences_in_period(self, period: Period) -> list[datetime.date]:
        """counts occurences in between dates"""


#    @abstractmethod
#    def expense_hits(self,date) -> bool:
#        """returns true if the expense hits on that day"""


class AnchoredExpenseSchedule(ExpenseSchedule):
    # def __init__(self,anchor:int=None, menu = None):
    #     super().__init__()
    #     if menu:
    #         self.menu = menu
    #         self.anchor = self.config()
    #     elif anchor:
    #         self.menu = None
    #         self.anchor = anchor
    #     else:
    #         raise ValueError('Called Improperly')
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

    # def config(self):
    #     anchor = self.menu().show_menu()
    #     print(f"Anchor: {anchor}")
    #     return int(anchor)


class FirstLastWorkingDayMonthlyExpenseSchedule(ExpenseSchedule):
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


class WeeklyExpenseSchedule(ExpenseSchedule):
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
