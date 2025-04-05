import json
from typing import Any
from menu_core import Menu, MenuEntry
from expense import Expense

class ExpenseTrackerApp:
    def __init__(self):
        self.expenses: list[Expense] = []

    def run(self) -> None:
        while True:
            menu = Menu("Main Menu", self.menu_config())
            result = menu.run()
            if result == {}:
                print("Goodbye!")
                break
    
    def menu_config(self) -> list[MenuEntry]:
        return [
            MenuEntry("Create Expense", self.create_expense),
            MenuEntry("View Expenses", self.view_expenses),
            MenuEntry("Delete Expenses", self.delete_expense),
            # Save and delete
        ]
    def create_expense(self) -> None:
        expense = Expense.run_menu()
        self.expenses.append(expense)
        print('Expense Added')

    def view_expenses(self) -> None:
        if not self.expenses:
            print("No Expenses.")
        else:
            for i, exp in enumerate(self.expenses, 1):
                print(f"{i}. {exp}")

    def delete_expense(self) -> None:
        if not self.expenses:
            print('No expenses.')
            return
        print('Select expense to delete')
        for i, exp in enumerate(self.expenses, 1):
            print(f"{i}. {exp}")
        choice = input(">>")
        if choice.isdigit():
            idx= int(choice) -1
            if 0 <= idx < len(self.expenses):
                del self.expenses[idx]
                print('Deleted.')
            else:
                print("Invalid Expense")
        else:
            print("Invalid Input.")

    # def save_file, def load_from_file

