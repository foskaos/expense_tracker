from schedule import Schedule
class Expense:

    def __init__(self, name:str, amount:float, schedule:Schedule):
        self.name = name
        self.amount = amount
        self.schedule = schedule


    def __repr__(self):
        return f"{self.name} ({self.amount}): Schedule {self.schedule}"
