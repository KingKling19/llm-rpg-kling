from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_navigation_state import (
    RestingHubNavigationState,
)

from llm_rpg.scenes.scene import Scene

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_state import (
        RestingHubState,
    )
    from llm_rpg.game.game import Game


class RestingHubScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.current_state = RestingHubNavigationState(self)

    def change_state(self, new_state: RestingHubState):
        self.current_state = new_state

    def handle_input(self):
        self.current_state.handle_input()

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
