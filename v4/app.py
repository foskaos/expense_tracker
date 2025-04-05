import json
from typing import Any
from form_core import Form, ChoiceField
from expense import Expense

class ExpenseTrackerApp(Form):
    def __init__(self):
        self.expenses: list[Expense] = []

        self.fields = [
            ChoiceField("main_menu", "Main Menu", {
                "1": self.create_expense,
                "2": self.view_expenses,
                "3": self.delete_expense,
                "4": self.save_to_file,
                "5": self.load_from_file
            })
        ]

    def run(self) -> None:
        while True:
            context = {}
            self.run_fields(context)
            if context.get("quit"):
                print("Goodbye!")
                break

    def create_expense(self) -> None:
        expense = Expense.run_form()
        self.expenses.append(expense)
        print("✅ Expense added.")

    def view_expenses(self) -> None:
        if not self.expenses:
            print("No expenses.")
        else:
            for i, exp in enumerate(self.expenses, 1):
                print(f"{i}. {exp}")
        input("\nPress Enter to return...")

    def delete_expense(self) -> None:
        if not self.expenses:
            print("No expenses.")
            return
        print("\nSelect an expense to delete:")
        for i, exp in enumerate(self.expenses, 1):
            print(f"{i}. {exp}")
        choice = input(">> ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.expenses):
                del self.expenses[idx]
                print("Deleted.")
            else:
                print("Invalid number.")
        else:
            print("Invalid input.")

    def save_to_file(self) -> None:
        filename = input("Enter filename: ")
        data = [e.to_dict() for e in self.expenses]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print("Saved.")

    def load_from_file(self) -> None:
        filename = input("Enter filename: ")
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.expenses = [Expense.from_dict(d) for d in data]
            print("Loaded.")
        except Exception as e:
            print(f"Failed to load: {e}")
