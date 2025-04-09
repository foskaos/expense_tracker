from dataclasses import dataclass, Field, field, fields
@dataclass
class Expense:
    name: str = field(metadata={'form_type':'prompt'})
    amount: str = field(metadata={'form_type':'prompt'})
    
class ModelForm:


    def __init__(self, model):
        for field in fields(model):
            print(field.metadata)
            
mf = ModelForm(Expense)
