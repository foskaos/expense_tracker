from categories import ExpenseCategory


class SelectionMenu:
    def __init__(self, selections: dict[str, str], title: str):
        self.selections = selections
        self.title = title

    def show_menu(self):
        title_padding = len(self.title) + 14
        print(f"{self.title:>{title_padding}}\n\n")
        for selector, display in self.selections.items():
            print(f"{selector:>15}: {display}")

        print("\n\n\n")

    def get_selection(self):
        selection = input("Select from the menu:")
        return self.selections[selection]

    def run(self):
        self.show_menu()
        selection = self.get_selection()
        return selection


class CategoryMenu(SelectionMenu):
    category_selection = {
        "r": ExpenseCategory.RENT,
        "g": ExpenseCategory.GROCERIES,
        "e": ExpenseCategory.EATING_OUT,
        "n": ExpenseCategory.ENTERTAINMENT,
        "u": ExpenseCategory.UTILITIES,
    }

    def __init__(self):
        super().__init__(self.category_selection, "Expense Category Selection")


class AnchoredExpenseMenu(SelectionMenu):
    sel_menu = {"1...28": "Enter a numbered day between 1 and 28"}
    valid_range = [str(i) for i in range(1, 29)]

    def __init__(self):
        super().__init__(self.sel_menu, "Recurring Expense Date")

    def show_menu(self):
        title_padding = len(self.title) + 14
        print(f"{self.title:>{title_padding}}\n\n")
        for selector, display in self.selections.items():
            print(f"{selector:>15}: {display}")

        print("\n\n\n")

    def get_selection(self):
        while True:
            selection = input("Select from the menu:")
            if selection in self.valid_range:
                return {"anchor": int(selection)}
            print("Invalid Selection")


class FLDayExpenseMenu(SelectionMenu):
    sel_menu = {"f": "First Working Day", "l": "Last Working Day"}

    def __init__(self):
        super().__init__(self.sel_menu, "First or Last Working Day of the Month")

    def get_selection(self):
        while True:
            selection = input("Select from the menu")
            if selection in ["f", "l"]:
                # TODO: this is arbitrary the dict. Should probably make an interface for this
                return {"anchor": selection}
            print("Invalid Selection.")


# class ScheduleMenu(SelectionMenu):
#    def __init__(self, selections):
#        super().__init__(selections, 'Expense Schedule Selection')
#
#    def run_wip(self):
#        # fixme: this should be more dynamic, eg. any number of nested menus should work.
#        selected = super().run()
#        sub = selected()
#        sub_sel = sub.run()
#        return sub_sel
