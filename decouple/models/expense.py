from models.schedule import Schedule


class Expense:
    def __init__(self, name: str, amount: float, schedule: Schedule):
        self.name = name
        self.amount = amount
        self.schedule = schedule

    def __repr__(self):
        return f"{self.name} ({self.amount}): Schedule {self.schedule}"

    @classmethod
    def from_dict(cls, input_dict):
        s = Schedule.from_dict(input_dict["schedule"])
        expense = cls(name=input_dict["name"], amount=input_dict["amount"], schedule=s)
        return expense

    def to_dict(self):
        output = {
            "name": self.name,
            "amount": self.amount,
            "schedule": self.schedule.to_dict(),
        }
        return output
