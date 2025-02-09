from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State
from llm_rpg.utils.rendering import render_state_transition_header
from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class RestingHubViewCharacterState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene

        self.last_user_navigation_input: UserNavigationInput = UserNavigationInput(
            -1, True
        )
        self.display_character_info = True
        self.display_state_transition_header = True

    def handle_input(self):
        self.last_user_navigation_input = get_user_navigation_input([0])

    def update(self):
        self.display_character_info = False
        self.display_state_transition_header = False
        if self.last_user_navigation_input.is_valid:
            if self.last_user_navigation_input.choice == 0:
                self.resting_hub_scene.game.change_scene(SceneTypes.RESTING_HUB)

    def _render_character(self):
        print(f"Name: {self.resting_hub_scene.game.hero.name}")
        print(f"Level: {self.resting_hub_scene.game.hero.level}")
        print(f"Class: {self.resting_hub_scene.game.hero.class_name}")

        print(f"Description: {self.resting_hub_scene.game.hero.description}")
        print("")
        print("Stats")
        print(f"Attack: {self.resting_hub_scene.game.hero.get_current_stats().attack}")
        print(
            f"Defense: {self.resting_hub_scene.game.hero.get_current_stats().defense}"
        )
        print(f"Focus: {self.resting_hub_scene.game.hero.get_current_stats().focus}")
        print(f"HP: {self.resting_hub_scene.game.hero.get_current_stats().max_hp}")
        print("")
        print("Equipped Items")
        if self.resting_hub_scene.game.hero.inventory.items:
            for item in self.resting_hub_scene.game.hero.inventory.items:
                print(f"  - {item.name} ({item.rarity.value}): {item.description}")
        else:
            print("No items equipped.")
        print("")

    def _render_ask_next_action(self):
        print("")
        print("What would you like to do next?")
        print("[0] to go back to the hub.")

    def _render_invalid_input(self):
        print("")
        print("Invalid input. You can only choose [0]")

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header("View Character")
        if self.display_character_info:
            self._render_character()
            self._render_ask_next_action()
        if not self.last_user_navigation_input.is_valid:
            self._render_invalid_input()
