from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

# TODO: fields should take a general interface rather than just hardcoded terminal

class Field(ABC):
    def __init__(self, name: str, label: str | None = None):
        self.name = name
        self.label = label or name

    @abstractmethod
    def run(self, context: dict[str, Any]) -> None: ...


class PromptField(Field):
    def __init__(self, name: str, label: str | None = None, cast: Callable[[str], Any] = str):
        super().__init__(name, label)
        self.cast = cast

    def run(self, context: dict[str, Any]) -> None:
        while True:
            try:
                value = self.cast(input(f"{self.label}: "))
                context[self.name] = value
                break
            except Exception:
                print("Invalid input.")

class NestedFormField(Field):
    def __init__(self, name: str, form: type, label: str | None = None):
        super().__init__(name, label or f"{name.title()} (Form)")
        self.form = form

    def run(self, context: dict[str, Any]) -> None:
        print(f"\n--- {self.label} ---")
        print(f"nested field context: {context}")
        context[self.name] = self.form.from_ui({})
        print(f"nested after form context: {context}")

class ChoiceField(Field):
    def __init__(self, name: str, label: str, choices: dict[str, Callable[[], None]]):
        super().__init__(name, label)
        self.choices = choices

    def run(self, context: dict[str, Any]) -> None:
        print(f"\n=== {self.label} ===")
        for key, action in self.choices.items():
            print(f"{key}. {action.__name__.replace('_', ' ').title()}")
        print("0. Quit")
        choice = input(">> ")
        if choice == "0":
            context["quit"] = True
        elif choice in self.choices:
            ret = self.choices[choice](context)
            if not self.name == "Main Menu":
                context[self.name] = ret
                print(f"CF ret: {ret}")
        else:
            print("Invalid choice.")
        print(f"CF Context: {context}")

class Form:
    #fields: list[Field] = []
    def __init__(self,fields):
        self.fields = fields

    def run_form(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        for field in self.fields:
            print(f"run field {field.name} with context: {context}")
            field.run(context)
            print(f'ran field {field.name} new context: {context}')
            if context.get("quit"):
                break
        print('finished form context:', context)
        return context  # Now returns the collected values, not an instance
#
# class Schedule:
# #    fields = [
# #        ChoiceField('Schedule Choice','type',{'a':lambda :print('anchor'), 'b':lambda :print('banchor')})
# #    ]
#     @classmethod
#     def from_ui(cls, context):
#         print(f'calling schedule ui with {context}')
#         choices = {sub.label[0]:sub.from_ui for sub in cls.__subclasses__()}
#         print(f'schedule choices: {choices}')
#         form = Form([ChoiceField('schedule','schedule builder',choices)])
#         context = form.run_form(context)
#         print(f"main schedule out{context}")
#         return context['schedule']
#
# class ASched(Schedule):
#     label = ('a','anchor')
#     fields = [
#         PromptField('anchor',label='Anchor Day'),
#         PromptField('title', label='Title')
#     ]
#
#     def __init__(self,anchor, title):
#         self.anchor = anchor
#         self.title = title
#     @classmethod
#     def from_ui(cls, context=None):
#         print('called a sched from ui')
#         context = context or {}
#         form = Form(cls.fields)
#         context = form.run_form(context)
#         print(f"a sched from ui out {context}")
#         return cls(**context)
#
#     def __repr__(self):
#         return f"Anchored Schedule {self.title} on {self.anchor}"
#
# class Expense:
#     fields = [
#         PromptField("name", 'Name'),
#         PromptField("amount", 'Amount'),
#         #PromptField("sched", 'Test'),
#         NestedFormField("schedule", Schedule, 'Schedule')
#     ]
#
#     def __init__(self,name, amount, schedule):
#         self.name = name
#         self.amount = amount
#         self.sched = schedule
#
#     @classmethod
#     def from_ui(cls, context):
#         form = Form(cls.fields)
#         context = form.run_form(context)
#         print(f'Expense Context: {context}')
#         return cls(**context)
#
#     def __repr__(self):
#         return f"{self.name}, for {self.amount} with {self.sched}"
# # def create_expense(context):
#     print(f'create_exp context before: {context}')
#     expense = Expense.from_ui({})
#     context['expenses'].append(expense)
#     print(f'create_exp context after: {context}')
#     return context
#
# def list_expenses(context):
#     for expense in context['expenses']:
#         print(expense)
# def main_menu(mm_context):
#
#
#     #mm_context = {'expenses':[]}
#     mm_choices = {
#         '1':create_expense,
#         #'2':inspect_contents
#         '2':list_expenses
#     }
#
#     form = Form(fields = [ChoiceField(name="Main Menu",label='This is the main menu', choices=mm_choices)])
#
#     mm_context = form.run_form(mm_context)
#     print(f"Main Menu context: {mm_context}")
#     return mm_context
# app_context = {'expenses':[]}
# while True:
#
#     app_context = main_menu(app_context)
#     import ipdb; ipdb.set_trace()
