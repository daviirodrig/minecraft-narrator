from enum import StrEnum

from pydantic import BaseModel


class BaseEventData(BaseModel):
    pass


class Event(StrEnum):
    ITEM_CRAFTED = "item_crafted"
    BLOCK_BROKEN = "block_broken"
    BLOCK_PLACED = "block_placed"
    PLAYER_DEATH = "player_death"
    ADVANCEMENT = "advancement"
    ITEM_PICKUP = "item_pickup"
    CHEST_CHANGE = "chest_change"
    ITEM_SMELTED = "item_smelted"
    MOB_KILLED = "mob_killed"
    DIMENSION_CHANGED = "dimension_changed"
    PLAYER_CHAT = "player_chat"
    PLAYER_ATE = "player_ate"
    JOIN_WORLD = "join_world"
    CONFIG = "config"


class IncomingEvent(BaseModel):
    event: Event
    data: str


# ==== Outgoing ====
class Action(StrEnum):
    IGNORE = "ignore"
    SEND_CHAT = "send_chat"


class OutgoingAction(BaseModel):
    action: Action
    data: str
