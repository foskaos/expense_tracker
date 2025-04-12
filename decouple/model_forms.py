from form import Form, PromptField, NestedFormField, ChoiceField, ChoiceDict, Choice
from models.expense import Expense
from models.schedule import (
    ASched,
    BSched,
    WeeklyExpenseSchedule,
    AnchoredExpenseSchedule,
)
import calendar

SCHEDULE_FORM_REGISTRY = ChoiceDict([])


def register_schedule_form(key):
    """Decorator to register a schedule form in the registry using a unique key."""

    def decorator(cls):
        choice = Choice(key, cls, cls.label)
        SCHEDULE_FORM_REGISTRY[key] = choice
        return cls

    return decorator


class ExpenseForm(Form):
    def __init__(self):
        super().__init__()
        self.fields = [
            PromptField("name", "Enter expense name"),
            PromptField("amount", "Enter expense amount"),
            NestedFormField("schedule", self.make_schedule_form, "Configure Schedule"),
        ]

    def make_schedule_form(self):
        choice_field = ChoiceField(
            "schedule_choice", "Select schedule type", SCHEDULE_FORM_REGISTRY
        )
        context = {}
        choice_field.get_input(context)
        form_class = context["schedule_choice"]

        return form_class().get_schedule()

    def get_expense(self):
        data = self.run_form()
        print(f"Got form data: {data}")
        return Expense(
            name=data["name"], amount=data["amount"], schedule=data["schedule"]
        )


@register_schedule_form("W")
class WeeklyScheduleForm(Form):
    label = "Weekly Schedule"

    def __init__(self):
        super().__init__()

        choices = [Choice(str(i), day, day) for i, day in enumerate(calendar.day_name)]

        self.fields = [
            ChoiceField("weekday", "Which Day of the Week?", ChoiceDict(choices))
        ]

    def week_day(self):
        choice_dict = {i: day for i, day in calendar.day_name()}
        choices = ChoiceField("weekday", "Which Day of the Week?", choice_dict)

    def get_schedule(self):
        print(f"called get_schedule for {self.__class__}")
        data = self.run_form()
        return WeeklyExpenseSchedule(weekday=data["weekday"])


@register_schedule_form("M")
class MonthlyAnchoredScheduleForm(Form):
    label = "Monthly Schedule"

    def __init__(self):
        super().__init__()
        self.fields = [
            PromptField(
                "anchor", "Enter day of the month (1-28)", int, (lambda x: 1 <= x <= 28)
            ),
        ]

    def get_schedule(self):
        data = self.run_form()
        return AnchoredExpenseSchedule(anchor=data["anchor"])
