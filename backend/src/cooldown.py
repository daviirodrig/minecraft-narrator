import time
from typing import Literal

from src.models import Event

CooldownType = Event | Literal["GLOBAL_COOLDOWN"]
CooldownsDict = dict[CooldownType, float]


class CooldownManager:
    def __init__(self):
        self.cooldowns: CooldownsDict = {}
        self.bypass_cooldowns: list[Event] = [
            Event.PLAYER_DEATH,
            Event.ADVANCEMENT,
            Event.DIMENSION_CHANGED,
            Event.PLAYER_CHAT,
        ]

    def add_cooldown(self, name: CooldownType, duration: int):
        self.cooldowns[name] = time.time() + duration

    def is_on_cooldown(self, name: CooldownType) -> bool:
        return time.time() < self.cooldowns.get(name, 0)

    def get_cooldown_remaining(self, name: CooldownType) -> int:
        remaining = self.cooldowns.get(name, 0) - time.time()
        return round(int(max(0, remaining)), 2)

    def reset_cooldown(self, name: CooldownType):
        self.cooldowns[name] = 0
