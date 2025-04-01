import unittest
from unittest.mock import patch, MagicMock, call
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the expense management module
from expense_manager import ExpenseManager, create_expense_form


class TestExpenseManager(unittest.TestCase):
    """Test the expense manager functionality"""
    
    def setUp(self):
        self.manager = ExpenseManager()
        
        # Create some mock expenses
        self.expense1 = MagicMock()
        self.expense1.name = "Rent"
        self.expense1.amount = 1000.0
        self.expense1.category = "Rent"
        
        self.expense2 = MagicMock()
        self.expense2.name = "Groceries"
        self.expense2.amount = 200.0
        self.expense2.category = "Groceries"
    
    def test_add_expense(self):
        self.manager.add_expense(self.expense1)
        self.assertEqual(len(self.manager.expenses), 1)
        self.assertEqual(self.manager.expenses[0], self.expense1)
    
    def test_total(self):
        self.manager.add_expense(self.expense1)
        self.manager.add_expense(self.expense2)
        self.assertEqual(self.manager.total(), 1200.0)
    
    def test_get_by_category(self):
        self.manager.add_expense(self.expense1)
        self.manager.add_expense(self.expense2)
        
        categories = self.manager.get_by_category()
        self.assertEqual(len(categories), 2)
        self.assertEqual(len(categories["Rent"]), 1)
        self.assertEqual(len(categories["Groceries"]), 1)
        self.assertEqual(categories["Rent"][0], self.expense1)
        self.assertEqual(categories["Groceries"][0], self.expense2)
    
    def test_generate_report(self):
        self.manager.add_expense(self.expense1)
        self.manager.add_expense(self.expense2)
        
        report = self.manager.generate_report()
        
        # Check that the report contains the expected number of lines
        self.assertEqual(len(report), 7)  # Header(2) + Separator(1) + Expenses(2) + Separator(1) + Total(1)
        
        # Check that the total appears in the last line
        self.assertTrue("1200.00" in report[-1] or "1200.0" in report[-1])
        
        # Check that expense names appear in the report
        report_text = '\n'.join(report)
        self.assertTrue("Rent" in report_text)
        self.assertTrue("Groceries" in report_text)


class TestCreateExpenseWithForm(unittest.TestCase):
    """Test the expense creation function"""
    
    @patch('form_integration.create_expense_form')
    @patch('form_integration.TerminalFormView')
    @patch('form_integration.Expense')
    def test_create_expense_with_form_anchored(self, MockExpense, MockTerminalFormView, mock_create_form):
        # Set up mocks
        mock_form = MagicMock()
        mock_create_form.return_value = mock_form
        
        mock_view = MagicMock()
        MockTerminalFormView.return_value = mock_view
        
        # Set up the form processing result
        mock_expense = MagicMock()
        mock_expense.name = "Test Expense"
        mock_expense.amount = 100.0
        mock_expense.category = "Test Category"
        mock_expense.anchor_day = "anchored_schedule"
        mock_expense.fl_anchor = None
        
        mock_view.process.return_value = mock_expense
        
        # Call the function
        result = create_expense_with_form()
        
        # Verify the correct mocks were created and called
        mock_create_form.assert_called_once()
        MockTerminalFormView.assert_called_once_with(mock_form)
        mock_view.process.assert_called_once()
        
        # Verify Expense was created with the right parameters
        MockExpense.assert_called_once_with(
            name="Test Expense",
            amount=100.0,
            category="Test Category",
            schedule="anchored_schedule"
        )
    
    @patch('form_integration.create_expense_form')
    @patch('form_integration.TerminalFormView')
    @patch('form_integration.Expense')
    def test_create_expense_with_form_fl(self, MockExpense, MockTerminalFormView, mock_create_form):
        # Set up mocks
        mock_form = MagicMock()
        mock_create_form.return_value = mock_form
        
        mock_view = MagicMock()
        MockTerminalFormView.return_value = mock_view
        
        # Set up the form processing result
        mock_expense = MagicMock()
        mock_expense.name = "Test Expense"
        mock_expense.amount = 100.0
        mock_expense.category = "Test Category"
        mock_expense.anchor_day = None
        mock_expense.fl_anchor = "fl_schedule"
        
        mock_view.process.return_value = mock_expense
        
        # Call the function
        result = create_expense_with_form()
        
        # Verify the correct mocks were created and called
        mock_create_form.assert_called_once()
        MockTerminalFormView.assert_called_once_with(mock_form)
        mock_view.process.assert_called_once()
        
        # Verify Expense was created with the right parameters
        MockExpense.assert_called_once_with(
            name="Test Expense",
            amount=100.0,
            category="Test Category",
            schedule="fl_schedule"
        )


@patch('form_integration.create_expense_with_form')
@patch('builtins.input')
@patch('builtins.print')
class TestMainFunction(unittest.TestCase):
    """Test the main application function"""
    
    def test_add_expense(self, mock_print, mock_input, mock_create_expense):
        # Set up mocks
        mock_input.side_effect = ["1", "3"]  # Add expense, then exit
        
        mock_expense = MagicMock()
        mock_expense.name = "Test Expense"
        mock_create_expense.return_value = mock_expense
        
        # Call the main function
        from form_integration import main
        main()
        
        # Verify the expense creation was called
        mock_create_expense.assert_called_once()
        
        # Verify appropriate output
        mock_print.assert_any_call(f"Added expense: Test Expense")
    
    def test_view_report_no_expenses(self, mock_print, mock_input, mock_create_expense):
        # Set up mocks
        mock_input.side_effect = ["2", "3"]  # View report, then exit
        mock_create_expense.return_value = None
        
        # Call the main function
        from form_integration import main
        main()
        
        # Verify appropriate output
        mock_print.assert_any_call("No expenses to report yet.")
    
    def test_invalid_choice(self, mock_print, mock_input, mock_create_expense):
        # Set up mocks
        mock_input.side_effect = ["invalid", "3"]  # Invalid choice, then exit
        
        # Call the main function
        from form_integration import main
        main()
        
        # Verify appropriate output
        mock_print.assert_any_call("Invalid choice. Please try again.")
    
    def test_keyboard_interrupt(self, mock_print, mock_input, mock_create_expense):
        # Set up mocks
        mock_input.side_effect = KeyboardInterrupt()
        
        # Call the main function
        from form_integration import main
        main()
        
        # Verify appropriate output
        mock_print.assert_called_with("\nProgram terminated by user.")


if __name__ == '__main__':
    unittest.main()