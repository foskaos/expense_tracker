from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Callable
import sys
class Menu(ABC):
    @abstractmethod
    def run(self):
        pass

@dataclass
class MenuOption:
    key: str
    short_text: str
    action: Callable | str

class SelectionMenu(Menu):

    def __init__(self, title, options):
        self.title = title
        self.options = options

    def process_input(self,user_input):
        
        options_as_dict = {option.key:option for option in self.options}

        selected_option = options_as_dict.get(user_input, None)

        if selected_option is None:
            raise ValueError('Invalid Selection')
        elif selected_option.action == 'value':
            return (lambda :selected_option.key)
        return selected_option.action

    def run(self):
        print(f"{self.title} Menu")
        for option in self.options:
            print(option)
            
        while True:
            user_input = input('Enter Choice')
            try:
                processed_input = self.process_input(user_input)
                break
            except ValueError as e:
                print(e)
                continue
        return processed_input() 

def create_report():
    return {'total':100, 'breakdown':['10']*10}

def create_schedule():
    
    def aschedule(*args):
        
        amenu_options = [
            MenuOption('a', short_text='Thing a', action="value"),
            MenuOption('b', short_text='Thing b', action="value")
        ]
        a_menu = SelectionMenu(title='Schedule A', options=amenu_options)
        a_menu.run()

        return ('ASchedule',args)
    
    def bschedule(*args):

        bmenu_options = [
            MenuOption('a', short_text='Thing a', action="value"),
            MenuOption('b', short_text='Thing b', action="value")
        ]
        b_menu = SelectionMenu(title='Schedule B', options=bmenu_options)
        b_menu.run()

        return ('BSchedule',args)

    sched_options = [
        MenuOption(key='a',short_text='A Sched', action=aschedule),
        MenuOption(key='b', short_text='B Sched', action=bschedule),
    ]

    smenu = SelectionMenu(title="Schedule Chooser", options=sched_options)
    smenu.run() 
def quit_app():
    print('quitting')
    sys.exit()

def create_expense():
    print('creating expense')
    create_schedule()
    return {'amount':100,'name':'money'}

mm_options = [
    MenuOption(key='a', short_text='Create Expense', action=create_expense),
    MenuOption(key='b', short_text='Make Report', action=create_report),
    MenuOption(key='e', short_text='Exit', action=quit_app)
]

main_menu = SelectionMenu(title='Main', options = mm_options)
main_menu.run()

