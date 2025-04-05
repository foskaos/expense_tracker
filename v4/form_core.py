from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

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
        context[self.name] = self.form.run_form()


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
            self.choices[choice]()
        else:
            print("Invalid choice.")


class Form:
    fields: list[Field] = []
    def run_fields(cls, context: dict[str, Any] | None = None) -> None:
        context = context or {}
        for field in cls.fields:
            field.run(context)
            if context.get("quit"):
                break

    @classmethod
    def run_form(cls, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        form = cls()
        form.run_fields(context)
        return context  # Now returns the collected values, not an instance
