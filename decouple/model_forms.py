from form import Form, PromptField, NestedFormField, ChoiceField
from models.expense import Expense
from models.schedule import Schedule, ASched, BSched
from typing import Any
SCHEDULE_FORM_REGISTRY = {}

def register_schedule_form(key):
    """Decorator to register a schedule form in the registry using a unique key."""
    def decorator(cls):
        SCHEDULE_FORM_REGISTRY[key] = cls
        return cls
    return decorator

# ------------------------------------------------------------------------------
# Define Forms Corresponding to the Models

class ExpenseForm(Form):
    def __init__(self):
        super().__init__()
        self.fields = [
            PromptField("name", "Enter expense name"),
            PromptField("amount", "Enter expense amount"),
            NestedFormField("schedule",self.make_schedule_form, "Configure Schedule" )
        ]

    def make_schedule_form(self):
        choice_field = ChoiceField("schedule_choice", "Select schedule type", SCHEDULE_FORM_REGISTRY)
        context = {}
        choice_field.get_input(context)  # Returns the chosen form class.
        form_class = context['schedule_choice']
        
        return form_class().get_schedule()

    def get_expense(self):
        data = self.run_form()
        print(f"Got form data: {data}")
        return Expense(
            name=data["name"],
            amount=data["amount"],
            schedule=data["schedule"]
        )

@register_schedule_form("W")
class WeeklyScheduleForm(Form):
    @staticmethod
    def label():
        return "Weekly Schedule"
    
    def __init__(self):
        super().__init__()
        self.fields = [
            PromptField("day", "Enter day of the week (e.g., Monday)"),
            PromptField("title", "Enter Schedule Title")
        ]

    def get_schedule(self):
        print(f'called get_schedule for {self.__class__}')
        data = self.run_form()
        return BSched(day=data["day"],title = data['title'])


@register_schedule_form("M")
class MonthlyScheduleForm(Form):
    @staticmethod
    def label():
        return "Monthly Schedule"
    
    def __init__(self):
        super().__init__()
        self.fields = [
            PromptField("anchor", "Enter day of the month (1-31)"),
            PromptField("title", "Enter Schedule Title")
        ]

    def get_schedule(self):
        data = self.run_form()
        return ASched(anchor=int(data["anchor"]), title=data['title'])

