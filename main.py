import datetime

from expenses import Expense
from menus import CategoryMenu
from period import Period
from builder import BuilderMenu



class Outgoings:
    def __init__(self):
        self.outs = []

    def add_outgoing(self, outgoing: Expense):
        self.outs.append(outgoing)

    def add_list_of_expenses(self, lst: list[Expense]):
        self.outs.extend(lst)

    def total(self) -> float:
        return sum(self.outs)


class Report:
    """
    Takes a list of set of outgoings and prints a nice report

    Constructs a report as a list of lines to be printed

    """

    def __init__(self, expenses: Outgoings):
        self.expenses = expenses

    # TODO: get longest line and make a single separator

    def header(self):
        title = f"{'name':<15}{'amount':<5}"
        separator = f"{'-' * len(title)}"
        return [title, separator]

    def table(self):
        lines = []
        for e in self.expenses.outs:
            line = f"{e.name:<15}{e.amount:<5}"
            lines.append(line)
        return lines

    def summary_row(self):
        summary = f"{'total':<15}{self.expenses.total()}"
        separator = f"{'-' * len(summary)}"
        return [separator, summary]

    def print_report(self):
        for row in self.header():
            print(row)
        for row in self.table():
            print(row)
        for row in self.summary_row():
            print(row)



def create_expense():
    # 1. Name
    # 2. Amount
    # 3. Category
    # 4. Schedule

    exp_name = input('Name:')
    exp_amount = input('Amount:')

    cat_sel_menu = CategoryMenu()
    exp_cat = cat_sel_menu.run()

    #exp_schedule_menu = ScheduleMenu()
    #exp_schedule_details = exp_schedule_menu.run()
    sched_builder = BuilderMenu().run()
    sched = sched_builder().run()
    
    # go through the appropriate menus for the schedule
    # exp_schedule = exp_schedule_class(menu = None)
    e = Expense(name=exp_name, amount=float(exp_amount), category=exp_cat, schedule=sched)
    return e


outgoings = Outgoings()
def add_expenses():
    while True:
    
        ne = create_expense()
        outgoings.add_outgoing(ne)

try:
    add_expenses()
except KeyboardInterrupt:
    print('done adding expenses')


    


