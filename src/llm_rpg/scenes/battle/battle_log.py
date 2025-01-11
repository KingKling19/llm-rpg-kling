from typing import Literal
from pydantic import BaseModel


class BattleAction(BaseModel):
    user: Literal["hero", "enemy"]
    action_description: str


class BattleLog:
    def __init__(self):
        self.actions = []

    def add_action(self, action: BattleAction):
        self.actions.append(action)

    def to_string(self, perspective: Literal["hero", "enemy"]):
        if perspective != "hero" and perspective != "enemy":
            raise ValueError("Invalid perspective")

        battle_log_text = ""
        for action in self.actions:
            if action.user == perspective:
                battle_log_text += f"You: {action.action_description}\n"
            else:
                battle_log_text += f"Enemy: {action.action_description}\n"
        return battle_log_text
