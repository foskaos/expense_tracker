from menu_core import MenuDriven, MenuEntry, prompt
from schedule import Schedule

class Expense(MenuDriven):
    def __init__(self, name: str, amount: float, schedule: Schedule):
        self.name = name
        self.amount = amount
        self.schedule = schedule

    def __str__(self) -> str:
        return f"{self.name} | ${self.amount:.2f} | {self.schedule.describe()}"

    def to_dict(self) -> dict[str, float | dict[str, str | int]]:
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
    def menu_config(cls) -> list[MenuEntry]:
        return [
            MenuEntry("Name", prompt("Name"), key="name"),
            MenuEntry("Amount", prompt("Amount", float), key="amount"),
            MenuEntry("Schedule", Schedule.pick_type_menu, key="schedule")
        ]
