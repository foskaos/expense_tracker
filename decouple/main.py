from model_forms import ExpenseForm

from form import ChoiceField, Form

#if __name__ == "__main__":
#    print("=== Expense Entry ===")
#    expense_form = ExpenseForm()
#    expense = expense_form.get_expense()
#    print("\nCreated expense:")
#    print(expense)
#
def create_expense(context):
    print("=== Expense Entry ===")
    expense_form = ExpenseForm()
    expense = expense_form.get_expense()
    print("\nCreated expense:")
    print(expense)
    context['expenses'].append(expense) 

class MainMenuForm(Form):
    pass
    """
    This would be a form where we present a set of choices to the user
    
    Maybe make a function choice field type

    could this be generalized?

    
    """
    def __init__(self, mm_choices):
        super().__init__()
        self.fields = [ChoiceField(name="MainMenu", label='This is the main menu', choices=mm_choices)]

    def do_menu_action(self,context):
        data = self.run_form(context)
        return data['MainMenu'](context)

def main_menu(mm_context):
    # mm_context = {'expenses':[]}
    mm_choices = {
        '1': create_expense,
        #'2':inspect_contents
        #'2': list_expenses
    }
    main_menu = MainMenuForm(mm_choices)
    main_menu.do_menu_action(mm_context) 
    # TODO: this is leaving the MainMenu Choice in the context... not sure if this is a problem
    print(f"Main Menu context: {mm_context}")
    return mm_context


app_context = {'expenses': []}
while True:
    app_context = main_menu(app_context)
