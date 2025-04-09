from model_forms import ExpenseForm, WeeklyScheduleForm, MonthlyScheduleForm


if __name__ == "__main__":
    print("=== Expense Entry ===")
    expense_form = ExpenseForm()
    expense = expense_form.get_expense()
    print("\nCreated expense:")
    print(expense)
