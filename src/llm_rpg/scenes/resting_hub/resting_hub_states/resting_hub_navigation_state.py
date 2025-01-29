from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_states import (
    RestingHubStates,
)
from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State
from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class RestingHubNavigationState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.has_updated = False
        self.last_user_navigation_input = UserNavigationInput(-1, False)
        self.massage_queue = []

    def handle_input(self):
        self.last_user_navigation_input = get_user_navigation_input([1, 2])

    def update(self):
        self.has_updated = True
        if self.last_user_navigation_input.is_valid:
            if self.last_user_navigation_input.choice == 1:
                self.resting_hub_scene.change_state(RestingHubStates.VIEW_CHARACTER)
            elif self.last_user_navigation_input.choice == 2:
                self.resting_hub_scene.game.change_scene(SceneTypes.BATTLE)
        else:
            self.massage_queue.append("Invalid input. Please enter [1] or [2].")

    def _render_message_queue(self):
        for message in self.massage_queue:
            print(message)
        self.massage_queue = []

    def render(self):
        if not self.has_updated:
            print("")
            print("Welcome to the resting hub!")
            print("INSERT ASCII ART HERE")
            print("What would you like to do?")
            print("[1] View Character")
            print("[2] Next Battle")
            print("Enter the number of your choice: ", end="")
        self._render_message_queue()
