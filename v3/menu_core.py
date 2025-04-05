from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

class MenuEntry:
    def __init__(self, label:str, action: Callable[[], Any], key: str | None = None):
        self.label = label
        self.action = action
        self.key = key
    def run(self, context: dict[str,Any]) -> None:
        result = self.action()
        if self.key:
            context[self.key] = result
        else:
            # put result in a generic key in the context
            context["result"] = result

class Menu:

    def __init__(self, title: str, entries: list[MenuEntry], back_option: bool = True):
        self.title = title
        self.entries = entries
        self.back_option = back_option

    def run(self, context: dict[str, Any] | None = None):
        if context is None:
            context = {}

        while True:
            print(f"{self.title} Menu")
            for i, entry in enumerate(self.entries, 1):
                print(f"{i}. {entry.label}")
            if self.back_option:
                print("0. Quit" if self.title == "Main Menu" else "0. Back")

            choice = input(">>")
            if choice == '0':
                return context
            elif choice.isdigit() and 1 <= int(choice) <= len(self.entries):
                entry = self.entries[int(choice) - 1] # -1 to index correctly agains the enumeration which starts at 1
                entry.run(context)
            else:
                print('Invalid Choice.')

def prompt(label: str, cast: Callable[[str], Any] = str) -> Callable[[], Any]:
    def runner() -> Any:
        while True:
            try:
                return cast(input(f"{label}: "))
            except:
                print('Invalid Input')
    return runner

def prompt_menu(label: str, cast: Callable[[str], Any] = str, key: str = 'value') -> Menu:
    return Menu(label,[MenuEntry(label, prompt(label,cast), key=key)], back_option=False)
        
class MenuDriven:
    @classmethod
    def run_menu(cls, context: dict[str,Any] | None = None) -> Any:
        menu = Menu(f"{cls.__name__} Menu", cls.menu_config())
        context = menu.run(context)
        return cls(**context)

