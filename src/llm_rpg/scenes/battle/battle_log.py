from typing import Literal
from pydantic import BaseModel


class BattleEvent(BaseModel):
    character_name: str
    proposed_action: str
    effect_description: str


class BattleLog:
    def __init__(self):
        self.actions = []

    def add_action(self, action: BattleEvent):
        self.actions.append(action)

    def to_string(self, n_actions: int = 5):
        battle_log_text = ""
        for action in self.actions[-n_actions:]:
            battle_log_text += (
                f"{action.character_name} turn: {action.effect_description}\n"
            )
        return battle_log_text
