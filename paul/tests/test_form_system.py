import unittest
from unittest.mock import patch, MagicMock

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the form system
from form_system import (
    Form, FormField, InputField, NumericField, SelectField,
    FormValidator, RangeValidator, ChoiceValidator,
    OutputTransformer, ScheduleTransformer
)


class TestFormValidator(unittest.TestCase):
    """Test the base validator functionality"""
    
    def test_validator_interface(self):
        # Create a simple concrete validator implementation
        class ConcreteValidator(FormValidator):
            def validate(self, value):
                return value == "valid"
        
        validator = ConcreteValidator("Custom error message")
        
        # Test validation logic
        self.assertTrue(validator.validate("valid"))
        self.assertFalse(validator.validate("invalid"))
        self.assertEqual(validator.error_message, "Custom error message")


class TestRangeValidator(unittest.TestCase):
    """Test the range validator"""
    
    def test_validate_in_range(self):
        validator = RangeValidator(1, 10)
        self.assertTrue(validator.validate(5))
        self.assertTrue(validator.validate("5"))  # Should handle string conversion
        self.assertTrue(validator.validate(1))    # Lower boundary
        self.assertTrue(validator.validate(10))   # Upper boundary
    
    def test_validate_out_of_range(self):
        validator = RangeValidator(1, 10)
        self.assertFalse(validator.validate(0))
        self.assertFalse(validator.validate(11))
        self.assertFalse(validator.validate("abc"))  # Invalid conversion
    
    def test_custom_error_message(self):
        validator = RangeValidator(1, 10, "Must be between 1 and 10")
        self.assertEqual(validator.error_message, "Must be between 1 and 10")


class TestChoiceValidator(unittest.TestCase):
    """Test the choice validator"""
    
    def test_validate_valid_choice(self):
        validator = ChoiceValidator(["a", "b", "c"])
        self.assertTrue(validator.validate("a"))
        self.assertTrue(validator.validate("b"))
        self.assertTrue(validator.validate("c"))
    
    def test_validate_invalid_choice(self):
        validator = ChoiceValidator(["a", "b", "c"])
        self.assertFalse(validator.validate("d"))
        self.assertFalse(validator.validate(""))
    
    def test_custom_error_message(self):
        validator = ChoiceValidator(["a", "b", "c"], "Pick one of the options")
        self.assertEqual(validator.error_message, "Pick one of the options")


class TestFormField(unittest.TestCase):
    """Test the base form field functionality"""
    
    def test_field_initialization(self):
        field = FormField("test_field", "input", "Test Field", True, "default", ["option1", "option2"])
        
        self.assertEqual(field.name, "test_field")
        self.assertEqual(field.field_type, "input")
        self.assertEqual(field.label, "Test Field")
        self.assertTrue(field.required)
        self.assertEqual(field.default, "default")
        self.assertEqual(field.options, ["option1", "option2"])
        self.assertEqual(field.validators[0].__class__, ChoiceValidator)  # Auto-created validator for options
    
    def test_field_validation_required(self):
        field = FormField("test_field", "input", required=True)
        
        # Empty value should fail for required field
        errors = field.validate("")
        self.assertTrue(len(errors) > 0)
        self.assertTrue("required" in errors[0].lower())
    
    def test_field_validation_with_validators(self):
        field = FormField("test_field", "input")
        field.add_validator(RangeValidator(1, 10))
        
        # Valid value
        self.assertEqual(field.validate(5), [])
        
        # Invalid value
        errors = field.validate(20)
        self.assertTrue(len(errors) > 0)
    
    def test_field_output_transformer(self):
        # Test with callable transformer
        field = FormField("test_field", "input")
        field.value = "test"
        field.set_output_transformer(lambda x: x.upper())
        
        self.assertEqual(field.get_transformed_value(), "TEST")
        
        # Test with OutputTransformer class
        class UppercaseTransformer(OutputTransformer):
            def transform(self, value):
                return value.upper()
        
        field.set_output_transformer(UppercaseTransformer())
        self.assertEqual(field.get_transformed_value(), "TEST")


class TestInputField(unittest.TestCase):
    """Test the input field functionality"""
    
    def test_input_field(self):
        field = InputField("name", "Full Name", True, "John Doe")
        
        self.assertEqual(field.name, "name")
        self.assertEqual(field.label, "Full Name")
        self.assertTrue(field.required)
        self.assertEqual(field.default, "John Doe")
        self.assertEqual(field.field_type, "input")


class TestNumericField(unittest.TestCase):
    """Test the numeric field functionality"""
    
    def test_numeric_field_with_range(self):
        field = NumericField("age", "Person's Age", True, 18, 0, 120)
        
        self.assertEqual(field.name, "age")
        self.assertEqual(field.label, "Person's Age")
        self.assertTrue(field.required)
        self.assertEqual(field.default, 18)
        self.assertEqual(field.field_type, "numeric")
        
        # Test the auto-created range validator
        self.assertEqual(field.validators[0].__class__, RangeValidator)
        self.assertEqual(field.validate(30), [])
        self.assertTrue(len(field.validate(150)) > 0)  # Over max
        self.assertTrue(len(field.validate(-5)) > 0)   # Under min


class TestSelectField(unittest.TestCase):
    """Test the select field functionality"""
    
    def test_select_field(self):
        options = {"r": "Red", "g": "Green", "b": "Blue"}
        field = SelectField("color", options, "Favorite Color", True, "r")
        
        self.assertEqual(field.name, "color")
        self.assertEqual(field.label, "Favorite Color")
        self.assertTrue(field.required)
        self.assertEqual(field.default, "r")
        self.assertEqual(field.field_type, "select")
        self.assertEqual(field.options, list(options.keys()))
        self.assertEqual(field.options_dict, options)
        
        # Test the auto-created choice validator
        self.assertEqual(field.validators[0].__class__, ChoiceValidator)
        self.assertEqual(field.validate("r"), [])
        self.assertTrue(len(field.validate("x")) > 0)  # Invalid option
    
    def test_select_field_transformed_value(self):
        options = {"r": "Red", "g": "Green", "b": "Blue"}
        field = SelectField("color", options)
        
        # Test that it retrieves the mapped value
        field.value = "r"
        self.assertEqual(field.get_transformed_value(), "Red")
        
        # Test with additional transformer
        field.set_output_transformer(lambda x: x.lower())
        self.assertEqual(field.get_transformed_value(), "red")


class TestForm(unittest.TestCase):
    """Test the form functionality"""
    
    def setUp(self):
        self.form = Form("Test Form")
        self.form.add_field(InputField("name", "Full Name", True))
        self.form.add_field(NumericField("age", "Age", True, None, 18, 100))
        self.form.add_field(SelectField("color", {"r": "Red", "g": "Green", "b": "Blue"}, "Favorite Color", False))
    
    def test_form_initialization(self):
        self.assertEqual(self.form.name, "Test Form")
        self.assertEqual(len(self.form.fields), 3)
    
    def test_form_validation(self):
        # Set valid values
        self.form.fields[0].value = "John Doe"
        self.form.fields[1].value = 25
        self.form.fields[2].value = "r"
        
        self.assertTrue(self.form.is_valid())
        self.assertEqual(self.form.validate(), {})
        
        # Set invalid value for age
        self.form.fields[1].value = 101
        self.assertFalse(self.form.is_valid())
        errors = self.form.validate()
        self.assertTrue("age" in errors)
    
    def test_form_get_data(self):
        # Set values
        self.form.fields[0].value = "John Doe"
        self.form.fields[1].value = 25
        self.form.fields[2].value = "r"
        
        data = self.form.get_data()
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(data["age"], 25)
        self.assertEqual(data["color"], "Red")  # Transformed by SelectField
    
    def test_form_submit_with_output_type(self):
        # Define a simple class to map to
        class Person:
            def __init__(self, name, age, color=None):
                self.name = name
                self.age = age
                self.color = color
        
        # Set values
        self.form.fields[0].value = "John Doe"
        self.form.fields[1].value = 25
        self.form.fields[2].value = "r"
        
        # Set output type
        self.form.set_output_type(Person)
        
        # Submit the form
        result = self.form.submit()
        
        # Check the result
        self.assertIsInstance(result, Person)
        self.assertEqual(result.name, "John Doe")
        self.assertEqual(result.age, 25)
        self.assertEqual(result.color, "Red")
    
    def test_form_submit_with_field_mapping(self):
        # Define a class with different parameter names
        class User:
            def __init__(self, username, user_age, favorite_color=None):
                self.username = username
                self.user_age = user_age
                self.favorite_color = favorite_color
        
        # Set values
        self.form.fields[0].value = "John Doe"
        self.form.fields[1].value = 25
        self.form.fields[2].value = "r"
        
        # Set output type with field mapping
        self.form.set_output_type(User, {
            "name": "username",
            "age": "user_age",
            "color": "favorite_color"
        })
        
        # Submit the form
        result = self.form.submit()
        
        # Check the result
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, "John Doe")
        self.assertEqual(result.user_age, 25)
        self.assertEqual(result.favorite_color, "Red")


class TestScheduleTransformer(unittest.TestCase):
    """Test the schedule transformer"""
    
    def test_schedule_transformer(self):
        # Mock a schedule class
        class MockSchedule:
            def __init__(self, anchor):
                self.anchor = anchor
        
        # Create a transformer
        transformer = ScheduleTransformer(MockSchedule)
        
        # Test transformation
        result = transformer.transform(42)
        self.assertIsInstance(result, MockSchedule)
        self.assertEqual(result.anchor, 42)


class TestExpenseForm(unittest.TestCase):
    """Test the expense form creation and processing"""
    
    @patch('form_system.AnchoredExpenseSchedule')
    @patch('form_system.FirstLastWorkingDayMonthlyExpenseSchedule')
    @patch('form_system.Expense')
    def test_create_expense_form(self, MockExpense, MockFLSchedule, MockAnchoredSchedule):
        # Set up mocks
        MockAnchoredSchedule.return_value = "anchored_schedule"
        MockFLSchedule.return_value = "fl_schedule"
        
        # Import and call the function
        from form_system import create_expense_form
        form = create_expense_form()
        
        # Basic form checks
        self.assertEqual(form.name, "Create Expense")
        self.assertEqual(len(form.fields), 5)
        self.assertEqual(form.output_type, MockExpense)
        
        # Test field transformations (without running the view)
        
        # First test anchored schedule
        anchor_field = next(f for f in form.fields if f.name == "anchor_day")
        anchor_field.value = "15"
        transformed = anchor_field.get_transformed_value()
        
        MockAnchoredSchedule.assert_called_once_with(15)
        
        # Then test FL schedule
        fl_field = next(f for f in form.fields if f.name == "fl_anchor")
        fl_field.value = "f"
        transformed = fl_field.get_transformed_value()
        
        MockFLSchedule.assert_called_once_with("f")


class TestTerminalFormView(unittest.TestCase):
    """Test the terminal form view"""
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_render_and_process(self, mock_print, mock_input):
        # Create a simple form
        form = Form("Test Form")
        form.add_field(InputField("name", "Name"))
        
        # Set up input mock to return a name
        mock_input.return_value = "John Doe"
        
        # Create the view and process it
        from form_system import TerminalFormView
        view = TerminalFormView(form)
        result = view.process()
        
        # Verify input was requested
        mock_input.assert_called_once()
        
        # Verify result contains the entered data
        self.assertEqual(result["name"], "John Doe")


if __name__ == '__main__':
    unittest.main()