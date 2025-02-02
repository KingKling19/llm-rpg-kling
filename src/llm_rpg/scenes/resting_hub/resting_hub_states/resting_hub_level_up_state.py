from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.objects.character import StatTypes
from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_states import (
    RestingHubStates,
)
from llm_rpg.scenes.state import State
from llm_rpg.utils.rendering import render_state_transition_header
from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class RestingHubLevelUpState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.message_queue = []
        self.last_user_navigation_input = UserNavigationInput(-1, False)
        self.render_level_up_message = True
        self.display_state_transition_header = True
        self.input_choice_stat_mapping = {
            1: StatTypes.ATTACK,
            2: StatTypes.DEFENSE,
            3: StatTypes.FOCUS,
            4: StatTypes.MAX_HP,
        }
        self.stat_increase_per_level = 5

    def handle_input(self):
        if self.resting_hub_scene.game.hero.should_level_up:
            self.last_user_navigation_input = get_user_navigation_input(
                list(self.input_choice_stat_mapping.keys())
            )

    def update(self):
        self.render_level_up_message = False
        self.display_state_transition_header = False
        if not self.resting_hub_scene.game.hero.should_level_up:
            self.resting_hub_scene.change_state(RestingHubStates.NAVIGATION)
        else:
            if self.last_user_navigation_input.is_valid:
                stat_type = self.input_choice_stat_mapping[
                    self.last_user_navigation_input.choice
                ]
                self.resting_hub_scene.game.hero.level_up(
                    stat_type, self.stat_increase_per_level
                )
                self.message_queue.append(
                    f"{stat_type.value} increased by {self.stat_increase_per_level}."
                )
            else:
                self.message_queue.append(
                    "Invalid input. Please enter [1] or [2] or [3] or [4]."
                )

    def _render_level_up_message(self):
        print("You have leveled up!")
        print("What would you like to increase?")
        print("[1] Attack")
        print("[2] Defense")
        print("[3] Focus")
        print("[4] HP")

    def _render_message_queue(self):
        for message in self.message_queue:
            print(message)
        self.message_queue = []

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header("Level Up")
        if self.render_level_up_message:
            self._render_level_up_message()
        self._render_message_queue()
