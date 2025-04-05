from form_core import Form, PromptField, NestedFormField
from schedule import Schedule

class Expense(Form):
    fields = [
        PromptField("name", "Name"),
        PromptField("amount", "Amount", cast=float),
        NestedFormField("schedule", Schedule)
    ]

    def __init__(self, name: str, amount: float, schedule: Schedule):
        self.name = name
        self.amount = amount
        self.schedule = schedule

    def __str__(self) -> str:
        return f"{self.name} | ${self.amount:.2f} | {self.schedule.describe()}"

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "amount": self.amount,
            "schedule": self.schedule.to_dict()
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> 'Expense':
        return cls(
            name=data["name"],
            amount=data["amount"],
            schedule=Schedule.from_dict(data["schedule"])
        )

    @classmethod
    def run_form(cls, context: dict[str, object] | None = None) -> 'Expense':
        context = super().run_form(context)  # Run Form.run_form(), which collects values
        return cls(**context)  # Now we safely construct the object with complete data
