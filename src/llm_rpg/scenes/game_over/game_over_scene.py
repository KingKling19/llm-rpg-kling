from __future__ import annotations

from typing import TYPE_CHECKING

from llm_rpg.scenes.game_over.game_over_states.game_over_end_screen_state import (
    GameOverEndScreenState,
)
from llm_rpg.scenes.game_over.game_over_states.game_over_states import GameOverStates
from llm_rpg.scenes.scene import Scene


if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class GameOverScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game=game)
        self.current_state = GameOverEndScreenState(self)

    def change_state(self, new_state: GameOverStates):
        if new_state == GameOverStates.END_SCREEN:
            self.current_state = GameOverEndScreenState(self)
