class ExpenseSchedule:
    pass

class AnchoredExpenseSchedule(ExpenseSchedule):
    def __init__(self, anchor):
        self.anchor = anchor

class FirstLastWorkingDayMonthlyExpenseSchedule(ExpenseSchedule):
    def __init__(self, anchor):
        self.anchor = anchor