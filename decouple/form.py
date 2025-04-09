from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

# TODO: fields should take a general interface rather than just hardcoded terminal

class Field(ABC):
    def __init__(self, name: str, label: str | None = None):
        self.name = name
        self.label = label

    @abstractmethod
    def get_input(self, context: dict[str, Any]) -> None: ...


class PromptField(Field):
    def __init__(self, name: str, label: str | None = None, cast: Callable[[str], Any] = str):
        super().__init__(name, label)
        self.cast = cast

    def get_input(self, context: dict[str, Any]) -> None:
        while True:
            try:
                value = self.cast(input(f"{self.label}: "))
                context[self.name] = value
                break
            except Exception:
                print("Invalid input.")

class NestedFormField(Field):
    def __init__(self, name: str, form: Callable, label: str | None = None):
        super().__init__(name, label)
        self.form = form

    def get_input(self, context: dict[str, Any]) -> None:
        print(f"\n--- {self.label} ---")
        # NOTE: form has to the the callable that runs the form and returns some kind of object
        context[self.name] = self.form()
        #print(f"nested after form context: {context}")

class ChoiceField(Field):
    def __init__(self, name: str, label: str, choices: dict[str, Callable[[], None]]):
        super().__init__(name, label)
        self.choices = choices

    def get_input(self, context: dict[str, Any]) -> None:
        # TODO: I don't like the numbered choices
        print(f"\n=== {self.label} ===")
        for key, action in self.choices.items():
            print(f"{key}. {action.__name__.replace('_', ' ').title()}")
        print("0. Quit")
        choice = input(">> ")
        if choice == "0":
            context["quit"] = True
        elif choice in self.choices:
            ret = self.choices[choice]
            # TODO: better way to handle main menu options
            if not self.name == "Main Menu":
                context[self.name] = ret
                #print(f"CF ret: {ret}")
        else:
            print("Invalid choice.")
        #print(f"CF Context: {context}")

class Form:
    #fields: list[Field] = []
    def __init__(self):
        self.fields = []

    def run_form(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        for field in self.fields:
            #print(f"run field {field.name} with context: {context}")
            field.get_input(context)
            #print(f'ran field {field.name} new context: {context}')
            if context.get("quit"):
                break
        #print('finished form context:', context)
        return context  # Now returns the collected values, not an instance
