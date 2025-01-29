from __future__ import annotations
from abc import ABC, abstractmethod

from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from llm_rpg.game.game import Game
    from llm_rpg.scenes.state import State


class SceneTypes(Enum):
    BATTLE = "battle"
    RESTING_HUB = "resting_hub"


class Scene(ABC):
    def __init__(self, game: Game, current_state: State):
        self.game = game
        self.current_state = current_state

    @abstractmethod
    def change_state(self, new_state: Enum):
        pass

    def handle_input(self):
        self.current_state.handle_input()

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
