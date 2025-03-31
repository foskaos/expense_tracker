from schedules import ExpenseSchedule
from categories import ExpenseCategory


class Expense:

    def __init__(self, amount: float, name: str, schedule: ExpenseSchedule, category: ExpenseCategory):
        self.amount = amount
        self.name = name
        self.schedule = schedule
        self.category = category

    def __add__(self, other):
        return self.amount + other.amount

    def __radd__(self, other):
        return self.amount + other

# class AnchoredExpense(Expense):
#
#     def __init__(self, amount, name, anchor):
#         self.name = name
#         self.amount = amount
#         self.anchor = anchor
