from abc import ABC, abstractmethod


class Menu(ABC):

    @abstractmethod
    def run(self) -> str:
        pass

class SelectionMenu(Menu):
    def __init__(self, title, name):
        self.title = title
        self.name = name

    def run(self):
        print(f'{self.title}:')
        print(f'get {self.name}>>   ')
        out = input(f'{self.name}>>   ')
        return out

class TextMenu:
    def __init__(self, title, name):
        self.title = title
        self.name = name


    def run(self):
        print(f'{self.title}')
        out = input(f'{self.name}>>   ')
        return out

class Schedule:

    def hits(self):
        pass


class ASchedule(Schedule):
    menu_config = [
    {
        'title': 'Anchor Day Schedule Menu',
        'name': 'anchor',
        'menu_type': 'text'
    }
    ]

    def __init__(self, anchor):
        self.anchor = anchor

    def hits(self):
        print(f'this is a Aschedule with {self.anchor}')

    def __repr__(self):
        return f'Anchor Day Schedule on {self.anchor}'


class FSchedule(Schedule):
    menu_config = [{
        'title': 'First Last Day Schedule Menu',
        'name': 'first_last_schedule',
        'menu_type': 'selection'
    },
    {
        'title': 'First Last Day Start Date Menu',
        'name': 'first_last_schedule_start',
        'menu_type': 'text'
    }]

    def __init__(self, first_last_schedule,first_last_schedule_start):
        print('called fsched constructor')
        self.fl = first_last_schedule
        self.sd = first_last_schedule_start

    def hits(self):
        print(f'this is a Fschedule with {self.fl}')

    def __repr__(self):
        return f'First Last Day on {self.fl} starting at {self.sd}'




def schedule_selection(inpt):
    sched_map = {'a': ASchedule,
             'f': FSchedule,
             'c': 'turd'}

    cons = sched_map[inpt]
    return cons

class Expense:

    def __init__(self, schedule:Schedule, amount:float):
        self.schedule = schedule
        self.amount = amount


class SFlow:

    def __init__(self, stages, target):
        self.stages = stages
        self.target = target

    def run(self):
        progress = {}
        for stage_entry in self.stages:
            name, stage, dispatcher = stage_entry
            user_input = stage.run()
            # problem with dispatch
            trans = dispatcher(user_input)
            if hasattr(trans, 'menu_config'):
                sub_menu_gathering = {}
                for menu in trans.menu_config:
                    config = {
                        'title': menu['title'],
                        'name': menu['name'],
                    }
                    if menu['menu_type'] == 'selection':
                        sub_menu = SelectionMenu(**config)
                    elif menu['menu_type'] == 'text':
                        sub_menu = TextMenu(**config)
                    sub_menu_gathering[menu['name']] = sub_menu.run()
                # print(sub_menu_gathering)
                out = trans(**sub_menu_gathering)
                # print(out)
                progress[name] = out
            else:
                progress[name] = trans

        print(progress)
        return self.target(**progress)


sm = SelectionMenu('Schedule choice Menu', 'schedule_type')
am = TextMenu('Amount Input Menu', 'amount')

f = SFlow([('amount',am,float),
           ('schedule',sm,schedule_selection)], Expense)
