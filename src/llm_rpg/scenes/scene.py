from __future__ import annotations
from abc import ABC

from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from llm_rpg.game.game import Game
    from llm_rpg.scenes.state import State


class SceneTypes(Enum):
    BATTLE = "battle"
    SHOP = "shop"
    MANAGE_CHARACTER = "manage_character"
    RESTING_HUB = "resting_hub"


class Scene(ABC):
    def __init__(self, game: Game):
        self.game = game

    def change_state(self, new_state: State):
        self.current_state = new_state

    def handle_input(self):
        self.current_state.handle_input()

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
