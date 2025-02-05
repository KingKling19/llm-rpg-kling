from __future__ import annotations

from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State

from typing import TYPE_CHECKING

from llm_rpg.utils.rendering import render_state_transition_header
from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.hero_creation.hero_creation_scene import HeroCreationScene


class HeroCreationChooseClassState(State):
    def __init__(self, scene: HeroCreationScene):
        self.scene = scene
        self.display_state_transition_header = True
        self.display_classes = True
        self.navigation_class_mapping = {
            1: scene.game.config.attack_hero_class,
            2: scene.game.config.defense_hero_class,
            3: scene.game.config.focus_hero_class,
        }
        self.last_user_navigation_input: UserNavigationInput | None = None

    def handle_input(self):
        self.last_user_navigation_input = get_user_navigation_input(
            self.navigation_class_mapping.keys()
        )

    def update(self):
        self.display_classes = False
        self.display_state_transition_header = False
        if self.last_user_navigation_input.is_valid:
            chosen_class = self.navigation_class_mapping[
                self.last_user_navigation_input.choice
            ]
            self.scene.game.hero.base_stats = chosen_class.base_stats
            self.scene.game.hero.description = chosen_class.description
            self.scene.game.hero.class_name = chosen_class.class_name
            self.scene.game.hero.inventory.add_item(chosen_class.starting_item)
            self.scene.game.change_scene(SceneTypes.RESTING_HUB)

    def _render_classes(self):
        print("Please select a class for your character:\n")
        for i, hero_class in enumerate(self.navigation_class_mapping.values()):
            print(f"[{i + 1}] Class: {hero_class.class_name}")
            print(f"    Description: {hero_class.description}")
            print(
                f"    Starting Item: {hero_class.starting_item.name}: {hero_class.starting_item.description}"
            )
            print("")

    def _render_invalid_choice(self):
        print("Invalid choice. Choose [1] [2] or [3]:")

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header(
                "Character Creation: Class",
            )
        if self.display_classes:
            self._render_classes()
        if (
            self.last_user_navigation_input
            and not self.last_user_navigation_input.is_valid
        ):
            self._render_invalid_choice()
