from menu_core import MenuDriven, Menu, MenuEntry, prompt
from abc import ABC, abstractmethod

class Schedule(MenuDriven, ABC):
    @abstractmethod
    def describe(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, str | int]: ...

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> 'Schedule':
        match data.get('type'):
            case 'daily':
                return DailySchedule.from_dict(data)
            case 'weekly':
                return WeeklySchedule.from_dict(data)
            case 'monthly':
                return MonthlySchedule.from_dict(data)
            case _:
                raise ValueError(f"Unknown schedule type: {data.get('type')}")

    @classmethod
    def pick_type_menu(cls) -> 'Schedule':
        menu = Menu("Choose Schedule Type", [
            MenuEntry("Daily", DailySchedule.run_menu),
            MenuEntry("Weekly", WeeklySchedule.run_menu),
            MenuEntry("Monthly", MonthlySchedule.run_menu)
        ])
        context = menu.run()
        return context.get("result")

class DailySchedule(Schedule):
    def __init__(self, time: str):
        self.time = time

    def describe(self) -> str:
        return f"Daily at {self.time}"

    def to_dict(self) -> dict[str, str]:
        return {'type': 'daily', 'time': self.time}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'DailySchedule':
        return cls(data['time'])

    @classmethod
    def menu_config(cls) -> list[MenuEntry]:
        return [MenuEntry("Time", prompt("Time (HH:MM)"), key="time")]

class WeeklySchedule(Schedule):
    def __init__(self, weekday: str, time: str):
        self.weekday = weekday
        self.time = time

    def describe(self) -> str:
        return f"Weekly on {self.weekday} at {self.time}"

    def to_dict(self) -> dict[str, str]:
        return {'type': 'weekly', 'weekday': self.weekday, 'time': self.time}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'WeeklySchedule':
        return cls(data['weekday'], data['time'])

    @classmethod
    def menu_config(cls) -> list[MenuEntry]:
        return [
            MenuEntry("Weekday", prompt("Weekday"), key="weekday"),
            MenuEntry("Time", prompt("Time (HH:MM)"), key="time")
        ]

class MonthlySchedule(Schedule):
    def __init__(self, day: int, time: str):
        self.day = day
        self.time = time

    def describe(self) -> str:
        return f"Monthly on day {self.day} at {self.time}"

    def to_dict(self) -> dict[str, str | int]:
        return {'type': 'monthly', 'day': self.day, 'time': self.time}

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> 'MonthlySchedule':
        return cls(int(data['day']), data['time'])

    @classmethod
    def menu_config(cls) -> list[MenuEntry]:
        return [
            MenuEntry("Day of Month", prompt("Day of Month", int), key="day"),
            MenuEntry("Time", prompt("Time (HH:MM)"), key="time")
        ]
