from abc import ABC, abstractmethod
from form_core import Form, PromptField

class Schedule(Form, ABC):
    @abstractmethod
    def describe(self) -> str: ...

    @abstractmethod
    def to_dict(self) -> dict[str, str | int]: ...

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> 'Schedule':
        match data.get('type'):
            case 'daily': return DailySchedule.from_dict(data)
            case 'weekly': return WeeklySchedule.from_dict(data)
            case 'monthly': return MonthlySchedule.from_dict(data)
            case _: raise ValueError(f"Unknown schedule type: {data.get('type')}")

class DailySchedule(Schedule):
    fields = [
        PromptField("time", "Time (HH:MM)")
    ]

    def __init__(self, time: str): self.time = time
    def describe(self) -> str: return f"Daily at {self.time}"
    def to_dict(self) -> dict[str, str]: return {"type": "daily", "time": self.time}
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'DailySchedule': return cls(data["time"])

class WeeklySchedule(Schedule):
    fields = [
        PromptField("weekday", "Weekday"),
        PromptField("time", "Time (HH:MM)")
    ]

    def __init__(self, weekday: str, time: str):
        self.weekday = weekday
        self.time = time

    def describe(self) -> str:
        return f"Weekly on {self.weekday} at {self.time}"

    def to_dict(self) -> dict[str, str]:
        return {"type": "weekly", "weekday": self.weekday, "time": self.time}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'WeeklySchedule':
        return cls(data["weekday"], data["time"])

class MonthlySchedule(Schedule):
    fields = [
        PromptField("day", "Day of Month", cast=int),
        PromptField("time", "Time (HH:MM)")
    ]

    def __init__(self, day: int, time: str):
        self.day = day
        self.time = time

    def describe(self) -> str:
        return f"Monthly on day {self.day} at {self.time}"

    def to_dict(self) -> dict[str, str | int]:
        return {"type": "monthly", "day": self.day, "time": self.time}

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> 'MonthlySchedule':
        return cls(int(data["day"]), data["time"])
