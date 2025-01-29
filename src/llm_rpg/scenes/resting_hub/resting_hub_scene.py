from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_level_up_state import (
    RestingHubLevelUpState,
)
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_navigation_state import (
    RestingHubNavigationState,
)

from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_states import (
    RestingHubStates,
)
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_view_character_state import (
    RestingHubViewCharacterState,
)
from llm_rpg.scenes.scene import Scene
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class RestingHubScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game=game, current_state=self.get_initial_state(game))

    def get_initial_state(self, game: Game) -> State:
        if game.hero.should_level_up:
            return RestingHubLevelUpState(self)
        else:
            return RestingHubNavigationState(self)

    def change_state(self, new_state: RestingHubStates):
        if new_state == RestingHubStates.NAVIGATION:
            self.current_state = RestingHubNavigationState(self)
        elif new_state == RestingHubStates.VIEW_CHARACTER:
            self.current_state = RestingHubViewCharacterState(self)
        elif new_state == RestingHubStates.LEVEL_UP:
            self.current_state = RestingHubLevelUpState(self)
