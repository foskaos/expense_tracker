from form_system import TerminalFormView, create_expense_form
from expenses import Expense
from categories import ExpenseCategory
from schedules import AnchoredExpenseSchedule, FirstLastWorkingDayMonthlyExpenseSchedule


class ExpenseManager:
    """Manages the collection of expenses and provides reporting functionality"""
    
    def __init__(self):
        self.expenses = []
    
    def add_expense(self, expense: Expense):
        """Add an expense to the collection"""
        self.expenses.append(expense)
    
    def total(self) -> float:
        """Calculate the total of all expenses"""
        return sum(expense.amount for expense in self.expenses)
    
    def get_by_category(self) -> dict:
        """Group expenses by category"""
        result = {}
        for expense in self.expenses:
            category = expense.category
            if category not in result:
                result[category] = []
            result[category].append(expense)
        return result
    
    def generate_report(self) -> list:
        """Generate a simple report of all expenses"""
        lines = []
        
        # Add header
        lines.append("Expense Report")
        lines.append("=" * 40)
        lines.append(f"{'Name':<20} {'Category':<15} {'Amount':>10}")
        lines.append("-" * 40)
        
        # Add expense lines
        for expense in self.expenses:
            lines.append(f"{expense.name:<20} {expense.category:<15} {expense.amount:>10.2f}")
        
        # Add summary
        lines.append("-" * 40)
        lines.append(f"{'Total':<35} {self.total():>10.2f}")
        
        return lines


def main():
    """Main application entry point"""
    manager = ExpenseManager()
    
    try:
        while True:
            print("\nExpense Management System")
            print("1. Add Expense")
            print("2. View Report")
            print("3. Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                # Create the form and view directly in the main function
                # This makes main() the composition root where objects are instantiated
                expense_form = create_expense_form()
                form_view = TerminalFormView(expense_form)
                
                # Process the form to get an expense
                expense = form_view.process()
                
                if expense:
                    manager.add_expense(expense)
                    print(f"Added expense: {expense.name}")
            elif choice == "2":
                if not manager.expenses:
                    print("No expenses to report yet.")
                else:
                    for line in manager.generate_report():
                        print(line)
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")


if __name__ == "__main__":
    main()