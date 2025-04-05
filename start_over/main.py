from expense import Expense
from menu_system import ChoiceField, Form

def create_expense(context):
    print(f'create_exp context before: {context}')
    expense = Expense.from_ui({})
    context['expenses'].append(expense)
    print(f'create_exp context after: {context}')
    return context


def list_expenses(context):
    for expense in context['expenses']:
        print(expense)


def main_menu(mm_context):
    # mm_context = {'expenses':[]}
    mm_choices = {
        '1': create_expense,
        # '2':inspect_contents
        '2': list_expenses
    }

    form = Form(fields=[ChoiceField(name="Main Menu", label='This is the main menu', choices=mm_choices)])

    mm_context = form.run_form(mm_context)
    print(f"Main Menu context: {mm_context}")
    return mm_context


app_context = {'expenses': []}
while True:
    app_context = main_menu(app_context)
