from menus import ScheduleMenu, AnchoredExpenseMenu, SelectionMenu

from schedules import AnchoredExpenseSchedule, schedule_menu_selections

class AnchoredScheduleBuilder:

    # 1. Select Schedule Type
    # 2. Run Schedule Specific Menu(s)
    def __init__(self):
        self.sched_class = AnchoredExpenseSchedule
        self.menu = AnchoredExpenseMenu

    def run(self):
        config = self.menu().run()
        return self.sched_class(config['anchor'])


menu_selections = {'a':AnchoredScheduleBuilder}


class BuilderMenu(SelectionMenu):
    def __init__(self):
        super().__init__(menu_selections, 'Build a Schedule')
