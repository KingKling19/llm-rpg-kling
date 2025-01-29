from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.resting_hub.resting_hub_states.resting_hub_states import (
    RestingHubStates,
)
from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class UserNavigationInput:
    def __init__(self, choice: int, is_valid: bool):
        self.choice = choice
        self.is_valid = is_valid


class RestingHubNavigationState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.has_updated = False
        self.last_user_navigation_input = UserNavigationInput(-1, False)
        self.massage_queue = []

    def _parse_input(self) -> UserNavigationInput:
        try:
            user_input = input().strip()
            choice = int(user_input)
            return UserNavigationInput(choice, True)
        except ValueError:
            return UserNavigationInput(-1, False)

    def handle_input(self):
        self.last_user_navigation_input = self._parse_input()

    def update(self):
        self.has_updated = True
        if self.last_user_navigation_input.is_valid:
            if self.last_user_navigation_input.choice == 1:
                self.resting_hub_scene.change_state(RestingHubStates.VIEW_CHARACTER)
            elif self.last_user_navigation_input.choice == 2:
                self.resting_hub_scene.game.change_scene(SceneTypes.BATTLE)
        else:
            self.massage_queue.append(
                "Invalid input. Please enter a number between 1 and 3."
            )

    def _render_message_queue(self):
        for message in self.massage_queue:
            print(message)
        self.massage_queue = []

    def render(self):
        if not self.has_updated:
            print("Welcome to the resting hub!")
            print("INSERT ASCII ART HERE")
            print("What would you like to do?")
            print("[1] View Character")
            print("[2] Next Battle")
            print("Enter the number of your choice: ", end="")
        self._render_message_queue()
