from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_states import (
    RestingHubStates,
)
from llm_rpg.scenes.state import State
from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class RestingHubLevelUpState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.has_updated = False
        self.message_queue = []
        self.last_user_navigation_input = UserNavigationInput(-1, False)

    def handle_input(self):
        if not self.has_updated:
            self.last_user_navigation_input = get_user_navigation_input([1, 2, 3, 4])

    def update(self):
        self.has_updated = True
        if not self.resting_hub_scene.game.hero.should_level_up:
            self.resting_hub_scene.change_state(RestingHubStates.NAVIGATION)
        else:
            if self.last_user_navigation_input.is_valid:
                if self.last_user_navigation_input.choice == 1:
                    self.resting_hub_scene.game.hero.stats.attack += 5
                    self.message_queue.append("Attack increased by 5.")
                elif self.last_user_navigation_input.choice == 2:
                    self.resting_hub_scene.game.hero.stats.defense += 5
                    self.message_queue.append("Defense increased by 5.")
                elif self.last_user_navigation_input.choice == 3:
                    self.resting_hub_scene.game.hero.stats.focus += 5
                    self.message_queue.append("Focus increased by 5.")
                elif self.last_user_navigation_input.choice == 4:
                    self.resting_hub_scene.game.hero.stats.hp += 5
                    self.message_queue.append("HP increased by 5.")
                self.resting_hub_scene.game.hero.should_level_up = False
            else:
                self.message_queue.append(
                    "Invalid input. Please enter [1] or [2] or [3] or [4]."
                )

    def _render_level_up_message(self):
        print("")
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
        if not self.has_updated:
            self._render_level_up_message()
        self._render_message_queue()
