from models.expense import Expense
from models.schedule import Schedule, WeeklyExpenseSchedule

# TODO: MAKE THIS INTO TESTS
ws = WeeklyExpenseSchedule("1")

print(ws)


wek = {"type": "weekly", "args": {"weekday": "2"}}

s = Schedule.from_dict(wek)
print(s)
print(s.to_dict())


ex = Expense(name="rent", amount=1000.0, schedule=s)

edict = ex.to_dict()
print(edict)
e3 = Expense.from_dict(edict)

print(e3)
