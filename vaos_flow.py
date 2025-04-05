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

class TextMenu(Menu):
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

    def __init__(self, stages, target, context, parent):
        self.stages = stages
        self.target = target
        self.context = context
        self.parent = parent

    def run(self):
        progress = {}
        for stage_entry in self.stages:
            name, stage, dispatcher = stage_entry
            user_input = stage.run()
            # problem with dispatch not sure this is a good idea.
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

        print(progress,self.target)
        #if self.target is None:
        #    return self
        if self.parent:
            return self.parent.run()
        print(self.target, 'called', self.target)
        if self.target is None:
            # this is weird, not sure when this would happen
            return
        return self.target(**progress)

context = None
sm = SelectionMenu('Schedule choice Menu', 'schedule_type')
am = TextMenu('Amount Input Menu', 'amount')

mm = SelectionMenu('Main Menu','main_menu')

def main_menu(input_choice):
    sel = {'1':f,
           '2':'exit'}
    print('running',f)
    sel[input_choice].run()
    return sel[input_choice]

mf = SFlow([('main',mm, main_menu)],None, context, None)


f = SFlow([('amount',am,float),
           ('schedule',sm,schedule_selection)], Expense, context,mf)



#f.run()
mflow = mf.run()

import ipdb; ipdb.set_trace()
#import ipdb; ipdb.set_trace()
# MAIN LOOP:

global_expenses = []

class ExpenseSet:

    def __init__(self, expenses):
        self.expenses = expenses

    def append_expense(self,expense):
        self.expenses.append(expense)

    def list_expenses(self):
        print(self.expensed)

#expense_flow = SFlow([
#        ('amount',am,float),
#        ('schedule',sm,schedule_selection)
#    ], Expense, context)
#
main_app = {'expenses':[],
            'app_name':'expense manager',
            }

main_menu_options = {'1':'create expense',
                     '2':'create report',
                     '3':'edit expenses',
                     '4':'save',
                     '5':'load'}




"""
once any main menu flow ends, return to main menu

so flows probably need a parent
"""
class SSchedule:
    def __init__(self,typ,anch):
        self.s_type = typ
        self.anchor = anch

    def __repr__(self):
        return f"{self.s_type} - {self.anchor}"
class Foo:

    def __init__(self, ui = False, **kwargs):
        if ui:
            self.name = self.name_menu()
            self.amount = self.amount_menu()
            self.schedule = self.schedule_menu()
        else:
            self.name = kwargs.get('name')
            self.amount = kwargs.get('amount')
            self.schedule = kwargs.get('schedule')
            
    def name_menu(self):
        print("enter a name")
        name = input('>>')
        return name
    
    def amount_menu(self):
        print('enter an amount')
        amount = input('>>')
        return amount
    
    def schedule_menu(self):
        print('choose schedule')
        stype = input('>>')
        if stype == 'a':
            print('anchor date?')
            anchor = input('>>')
        return SSchedule(stype, anchor)


bar = Foo(ui=True)

foobar = Foo(name='ha', amount='100', schedule=('s','s'))

import ipdb; ipdb.set_trace()


