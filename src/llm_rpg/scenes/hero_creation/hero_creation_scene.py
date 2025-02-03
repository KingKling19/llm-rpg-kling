from __future__ import annotations

from typing import TYPE_CHECKING

from llm_rpg.scenes.hero_creation.hero_creation_states.hero_creation_states import (
    HeroCreationStates,
)
from llm_rpg.scenes.scene import Scene


if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class HeroCreationScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game=game)
        self.current_state = None

    def change_state(self, new_state: HeroCreationStates):
        pass
