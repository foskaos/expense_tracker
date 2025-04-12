from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

# TODO: fields should take a general interface rather than just hardcoded terminal


class Choice:
    def __init__(self, key, value, label):
        print("this is a choice")
        self.key = key
        self.value = value
        self.label = label


class ChoiceDict:
    def __init__(self, choices):
        self._choices = choices
        self._index = {choice.key: choice for choice in choices}

    def __getitem__(self, key):
        return self._index[key]

    def __setitem__(self, key, value):
        self._index[key] = value

    def __contains__(self, key):
        return key in self._index

    def __iter__(self):
        return iter(self._index)

    def items(self):
        return self._index.items()

    def keys(self):
        return self._index.keys()

    def values(self):
        return self._index.values()

    def __len__(self):
        return len(self._index)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._index})"


class Field(ABC):
    def __init__(self, name: str, label: str | None = None):
        self.name = name
        self.label = label

    @abstractmethod
    def get_input(self, context: dict[str, Any]) -> None: ...


class PromptField(Field):
    def __init__(
        self,
        name: str,
        label: str | None = None,
        cast: Callable[[str], Any] = str,
        validator: Callable = None,
    ):
        super().__init__(name, label)
        self.cast = cast
        self.validator = validator

    def get_input(self, context: dict[str, Any]) -> None:
        while True:
            try:
                value = self.cast(input(f"{self.label}: "))
                if self.validator:
                    if not self.validator(value):
                        raise Exception()

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


class ChoiceField(Field):
    def __init__(self, name: str, label: str, choices: ChoiceDict):
        super().__init__(name, label)
        self.choices = choices

    def get_input(self, context: dict[str, Any]) -> None:
        # TODO: I don't like the numbered choices
        print(f"\n=== {self.label} ===")
        for key, choice in self.choices.items():
            print(f"{key}: {choice.label}")
        # print("0. Quit")
        choice = input(">> ")
        # if choice == "0":
        #    print('user wants to go!!')
        #    context["quit"] = True
        # elif choice in self.choices:
        if choice in self.choices:
            ret = self.choices[choice].value
        else:
            print("Invalid choice.")


class Form:
    def __init__(self):
        self.fields = []

    def run_form(self, context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        for field in self.fields:
            field.get_input(context)
            if context.get("quit"):
                break
        return context  # Now returns the collected values, not an instance
