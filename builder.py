from menus import AnchoredExpenseMenu, SelectionMenu, FLDayExpenseMenu

from schedules import AnchoredExpenseSchedule, FirstLastWorkingDayMonthlyExpenseSchedule

class AnchoredScheduleBuilder:

    # 1. Select Schedule Type
    # 2. Run Schedule Specific Menu(s)
    def __init__(self):
        self.sched_class = AnchoredExpenseSchedule
        self.menu = AnchoredExpenseMenu()

    def run(self):
        config = self.menu.run()
        return self.sched_class(config['anchor'])

class FLScheduleBuilder:

    def __init__(self):
        self.sched_class = FirstLastWorkingDayMonthlyExpenseSchedule
        self.menu = FLDayExpenseMenu()

    def run(self):
        config = self.menu.run()
        return self.sched_class(config['anchor'])

menu_selections = {'a':AnchoredScheduleBuilder,
                   'f':FLScheduleBuilder}


class BuilderMenu(SelectionMenu):
    def __init__(self):
        super().__init__(menu_selections, 'Build a Schedule')
