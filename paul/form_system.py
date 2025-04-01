from typing import Callable, List, Dict, Any, Type, Optional, Union
from abc import ABC, abstractmethod


class OutputTransformer:
    """Base class for transforming form field values before final output"""
    
    @abstractmethod
    def transform(self, value: Any) -> Any:
        """Transform the input value into the desired output format"""
        pass


class FormValidator:
    """Base class for form field validation"""
    
    def __init__(self, error_message: str = "Invalid input"):
        self.error_message = error_message
    
    @abstractmethod
    def validate(self, value: Any) -> bool:
        """Validate the input value. Return True if valid, False otherwise."""
        pass


class RangeValidator(FormValidator):
    """Validates that a numeric input is within a specified range"""
    
    def __init__(self, min_value: float, max_value: float, error_message: str = None):
        super().__init__(error_message or f"Value must be between {min_value} and {max_value}")
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value: Any) -> bool:
        try:
            num_value = float(value)
            return self.min_value <= num_value <= self.max_value
        except (ValueError, TypeError):
            return False


class ChoiceValidator(FormValidator):
    """Validates that an input is one of a set of valid choices"""
    
    def __init__(self, valid_choices: List[Any], error_message: str = None):
        super().__init__(error_message or f"Value must be one of: {', '.join(str(c) for c in valid_choices)}")
        self.valid_choices = valid_choices
    
    def validate(self, value: Any) -> bool:
        return value in self.valid_choices


class FormField:
    """Base class for form fields"""
    
    def __init__(self, name: str, field_type: str, label: str = None, required: bool = True, 
                 default: Any = None, options: List[Any] = None):
        self.name = name
        self.field_type = field_type
        self.label = label or name.replace('_', ' ').capitalize()
        self.required = required
        self.default = default
        self.options = options
        self.validators: List[FormValidator] = []
        self.output_transformer: Optional[Union[OutputTransformer, Callable]] = None
        self.value = None
        
        # Add default validator for options if provided
        if options:
            self.add_validator(ChoiceValidator(options))
    
    def add_validator(self, validator: FormValidator) -> 'FormField':
        """Add a validator to this field"""
        self.validators.append(validator)
        return self
    
    def set_output_transformer(self, transformer: Union[OutputTransformer, Callable]) -> 'FormField':
        """Set a transformer for the field's output value"""
        self.output_transformer = transformer
        return self
    
    def validate(self, value: Any) -> List[str]:
        """Validate the field value against all validators"""
        if self.required and (value is None or value == ''):
            return [f"{self.label} is required"]
        
        errors = []
        for validator in self.validators:
            if not validator.validate(value):
                errors.append(validator.error_message)
        
        return errors
    
    def get_transformed_value(self) -> Any:
        """Get the transformed value for output"""
        if self.value is None:
            return self.default
        
        if self.output_transformer:
            if isinstance(self.output_transformer, OutputTransformer):
                return self.output_transformer.transform(self.value)
            else:
                return self.output_transformer(self.value)
        
        return self.value


class InputField(FormField):
    """Standard text input field"""
    
    def __init__(self, name: str, label: str = None, required: bool = True, default: str = None):
        super().__init__(name, 'input', label, required, default)


class NumericField(FormField):
    """Numeric input field"""
    
    def __init__(self, name: str, label: str = None, required: bool = True, 
                 default: float = None, min_value: float = None, max_value: float = None):
        super().__init__(name, 'numeric', label, required, default)
        
        if min_value is not None and max_value is not None:
            self.add_validator(RangeValidator(min_value, max_value))


class SelectField(FormField):
    """Selection field with predefined options"""
    
    def __init__(self, name: str, options: Dict[str, Any], label: str = None, 
                 required: bool = True, default: str = None):
        self.options_dict = options
        super().__init__(name, 'select', label, required, default, list(options.keys()))
    
    def get_transformed_value(self) -> Any:
        """Get the transformed value, mapped through the options dictionary"""
        if self.value is None:
            return self.default
        
        # First get the value from the options dict
        if self.value in self.options_dict:
            value = self.options_dict[self.value]
        else:
            value = self.value
        
        # Then apply any additional transformer
        if self.output_transformer:
            if isinstance(self.output_transformer, OutputTransformer):
                return self.output_transformer.transform(value)
            else:
                return self.output_transformer(value)
        
        return value


class Form:
    """Encapsulates the core functionality of a form - defines fields and options, processes data and produces output"""
    
    def __init__(self, name: str = "Form"):
        self.name = name
        self.fields: List[FormField] = []
        self.output_type: Optional[Type] = None
        self.field_map: Optional[Dict[str, str]] = None
    
    def add_field(self, field: FormField) -> 'Form':
        """Add a field to the form"""
        self.fields.append(field)
        return self
    
    def set_output_type(self, output_type: Type, field_map: Dict[str, str] = None) -> 'Form':
        """Set custom object type for the output"""
        self.output_type = output_type
        self.field_map = field_map
        return self
    
    def validate(self) -> Dict[str, List[str]]:
        """Validate all fields and return any validation errors"""
        errors = {}
        
        for field in self.fields:
            field_errors = field.validate(field.value)
            if field_errors:
                errors[field.name] = field_errors
        
        return errors
    
    def is_valid(self) -> bool:
        """Check if all fields are valid"""
        return len(self.validate()) == 0
    
    def get_data(self) -> Dict[str, Any]:
        """Get all field values as a dictionary"""
        return {field.name: field.get_transformed_value() for field in self.fields}
    
    def submit(self) -> Any:
        """Process form data and return as the specified output type or a dictionary"""
        if not self.is_valid():
            raise ValueError("Form has validation errors. Call is_valid() before submitting.")
        
        data = self.get_data()
        
        if self.output_type:
            if self.field_map:
                # Map field names to the constructor parameter names
                kwargs = {target: data[source] for source, target in self.field_map.items()}
                # Add any fields not in the mapping that have matching names
                for field_name in data:
                    if field_name not in self.field_map:
                        kwargs[field_name] = data[field_name]
            else:
                # Assume field names match constructor parameter names
                kwargs = data
            
            return self.output_type(**kwargs)
        
        return data


class FormView(ABC):
    """Base class for form rendering and interaction"""
    
    def __init__(self, form: Form):
        self.form = form
    
    @abstractmethod
    def render(self) -> None:
        """Render the form"""
        pass
    
    @abstractmethod
    def process(self) -> Any:
        """Process form submission and return result"""
        pass


class TerminalFormView(FormView):
    """Terminal-based form view"""
    
    def __init__(self, form: Form):
        super().__init__(form)
    
    def render(self) -> None:
        """Render the form in the terminal"""
        print(f"\n--- {self.form.name} ---\n")
        
        for field in self.form.fields:
            self._render_field(field)
    
    def _render_field(self, field: FormField) -> None:
        """Render a single form field"""
        prompt = f"{field.label}"
        if field.required:
            prompt += " *"
        
        if field.field_type == 'select' and field.options:
            print(f"\n{prompt}:")
            for i, option in enumerate(field.options):
                print(f"  {option}: {field.options_dict.get(option, option)}")
                
            while True:
                value = input(f"> ").strip()
                if not value and field.default:
                    value = field.default
                
                field.value = value
                errors = field.validate(value)
                if not errors:
                    break
                
                for error in errors:
                    print(f"Error: {error}")
        else:
            default_display = f" [{field.default}]" if field.default is not None else ""
            while True:
                value = input(f"{prompt}{default_display}: ").strip()
                if not value and field.default is not None:
                    value = field.default
                
                if field.field_type == 'numeric':
                    try:
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                    except ValueError:
                        print("Error: Please enter a numeric value.")
                        continue
                
                field.value = value
                errors = field.validate(value)
                if not errors:
                    break
                
                for error in errors:
                    print(f"Error: {error}")
    
    def process(self) -> Any:
        """Process form submission"""
        self.render()
        try:
            if self.form.is_valid():
                return self.form.submit()
            else:
                print("\nThere were validation errors. Please correct them and try again.")
                return None
        except ValueError as e:
            print(f"Error: {e}")
            return None


# Transformers for your specific application

class ScheduleTransformer(OutputTransformer):
    """Transform anchor selections into the appropriate schedule objects"""
    
    def __init__(self, schedule_type):
        self.schedule_type = schedule_type
    
    def transform(self, value: Any) -> Any:
        """Create a schedule object from the provided value"""
        return self.schedule_type(value)


# Integration example for expense form
def create_expense_form():
    """Create a form for expense input"""
    from expenses import Expense
    from categories import ExpenseCategory
    from schedules import AnchoredExpenseSchedule, FirstLastWorkingDayMonthlyExpenseSchedule
    
    form = Form("Create Expense")
    
    # Basic expense info
    form.add_field(InputField("name", "Expense Name"))
    form.add_field(NumericField("amount", "Amount", min_value=0.01))
    
    # Category selection
    form.add_field(SelectField(
        "category", 
        {
            "r": ExpenseCategory.RENT,
            "g": ExpenseCategory.GROCERIES,
            "e": ExpenseCategory.EATING_OUT,
            "n": ExpenseCategory.ENTERTAINMENT,
            "u": ExpenseCategory.UTILITIES,
        },
        "Category"
    ))
    
    # Schedule type selection
    schedule_type_field = SelectField(
        "schedule_type",
        {
            "a": "Anchored (monthly on specific day)",
            "f": "First/Last Working Day of Month"
        },
        "Schedule Type"
    )
    form.add_field(schedule_type_field)
    
    # Conditional fields based on schedule type
    anchored_field = NumericField(
        "anchor_day", 
        "Day of Month (1-28)", 
        required=False,
        min_value=1, 
        max_value=28
    )
    # Transform the day number into an actual schedule
    anchored_field.set_output_transformer(
        lambda value: AnchoredExpenseSchedule(int(value))
    )
    form.add_field(anchored_field)
    
    fl_field = SelectField(
        "fl_anchor",
        {
            "f": "First Working Day",
            "l": "Last Working Day"
        },
        "First or Last", 
        required=False
    )
    # Transform the f/l selection into an actual schedule
    fl_field.set_output_transformer(
        lambda value: FirstLastWorkingDayMonthlyExpenseSchedule(value)
    )
    form.add_field(fl_field)
    
    # Set up the output type to be an Expense object
    form.set_output_type(
        Expense,
        {
            # Map from form field name to Expense constructor param name where they differ
            "anchor_day": "schedule",
            "fl_anchor": "schedule"
        }
    )
    
    return form