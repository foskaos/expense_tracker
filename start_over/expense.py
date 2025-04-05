from menu_system import Form, PromptField, NestedFormField
from schedule import Schedule

class Expense:
    # fields = [
    #     PromptField("name", 'Name'),
    #     PromptField("amount", 'Amount'),
    #     #PromptField("sched", 'Test'),
    #     NestedFormField("schedule", Schedule, 'Schedule')
    # ]

    def __init__(self,name, amount, schedule):
        self.name = name
        self.amount = amount
        self.sched = schedule

    @classmethod
    def from_ui(cls, context):
        form = Form(cls.fields)
        context = form.run_form(context)
        print(f'Expense Context: {context}')
        return cls(**context)

    def __repr__(self):
        return f"{self.name}, for {self.amount} with {self.sched}"

class ExpenseForm(Form):
    fields = [
        PromptField("name", 'Name',  input_handler: Callable[[str], str]),
        PromptField("amount", 'Amount'),
    ]
    @classmethod
    def from_ui(cls, context):
        form = Form(Expense.fields)
        context = form.run_form(context)
        print(f'Expense Context: {context}')
        return cls(**context)


class SchedukeOptions:

