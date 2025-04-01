from dataclasses import dataclass

att = {'name':{'keybind':'a',
               'selection':'?'}}# not sure here. i want this to be dynamic}}



class AttibuteMenu:

    def __init__(self, attribute):
        self.attribute = attribute

class Builder:

    def __init__(self, config, c):
        self.config = config
        self.c = c


# sample 'flow'
# create expense
# 'welcome screen'
# load file
# save file
class Menu:

    def __init__(self, config):
        self.config = config

    def run(self):
        print(f"{self.config['title']}")
        # show actions
        print(f"actions:\n")
        # prompt
        action = input('>   ')

        return action


flow = [
    {'title':'ha',
     'input_range':['a','b','c'],
     }
]

'''
multiple choice of values (kind of schedule)
true false
free input (eg amount)
always get an actual string.

need some way to map from input string to whatever is desired by a builder


a menu needs:
title: str
list of:
    key, description, choice

how do we process that input we get that corresponds to a choice
eg:
for a schedule:
a, anchored schedule, anchored schedule
f, first day of the month, first day schedule
...

need a way to transform a user input into something useful

eg amount will be a string like '100' that needs to be changed into a float

eg anchored schedule menu will get something like a number from 1...28, but that will be just a string, so that needs at least a conversion to int, then to be passed to a schedule constructor.

so interface would be string -> instance of some class (for amount 'class' is float for achored schedule, class is anchoredexpenseschedule)


'''
class UserInput:
    def validate_input(self,input: str) -> bool:
        pass

class UserSelection(UserInput):
    pass


class UserText(UserInput):
    pass

class UserMenu:

    def run(self) -> UserInput:
        pass

class MenuConfig:

    def __init__(self):
        pass

@dataclass
class MenuAction:
    key: str
    display: str


class Test:

    def __init__(self,string, target: type):
        self.string = string
        self.target = target

    def action(self):
        print(self.target(self.string))


import ipdb; ipdb.set_trace()
