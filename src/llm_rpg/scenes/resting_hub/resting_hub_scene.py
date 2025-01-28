from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_navigation_state import (
    RestingHubNavigationState,
)

from llm_rpg.scenes.scene import Scene

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class RestingHubScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.current_state = RestingHubNavigationState(self)
