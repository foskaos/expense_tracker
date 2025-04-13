from model_forms import ExpenseForm
import sys

from form import ChoiceField, Form, Choice, ChoiceDict


def create_expense(context):
    print("=== Expense Entry ===")
    expense_form = ExpenseForm()
    expense = expense_form.get_expense()
    print("\nCreated expense:")
    print(expense)
    context["expenses"].append(expense)


class MainMenuForm(Form):
    pass
    """
    This would be a form where we present a set of choices to the user
    
    Maybe make a function choice field type

    could this be generalized?

    
    """

    def __init__(self, mm_choices):
        super().__init__()
        self.fields = [
            ChoiceField(
                name="MainMenu", label="This is the main menu", choices=mm_choices
            )
        ]

    def do_menu_action(self, context):
        data = {}
        data = self.run_form(data)
        return data["MainMenu"](context)


def quit(*args, **kwargs):
    sys.exit(0)


def main_menu(mm_context):
    # mm_context = {'expenses':[]}
    mm_choices = ChoiceDict(
        [
            Choice("1", create_expense, "Make an expense"),
            Choice("q", quit, "Quit"),
        ]
    )
    main_menu = MainMenuForm(mm_choices)
    main_menu.do_menu_action(mm_context)
    print(f"Main Menu context: {mm_context}")
    return mm_context


app_context = {"expenses": []}
while True:
    app_context = main_menu(app_context)
