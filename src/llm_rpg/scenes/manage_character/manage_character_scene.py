from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.scenes.manage_character.manage_character_states.manage_character_view_state import (
    ManageCharacterViewState,
)
from llm_rpg.scenes.scene import Scene

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class ManageCharacterScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.current_state = ManageCharacterViewState(self)
