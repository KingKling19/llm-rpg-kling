from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.manage_character.manage_character_states.manage_character_state import (
    ManageCharacterState,
)
from llm_rpg.scenes.scene import SceneTypes

if TYPE_CHECKING:
    from llm_rpg.scenes.manage_character.manage_character_scene import (
        ManageCharacterScene,
    )


class ManageCharacterViewInput:
    def __init__(self, choice: int, is_valid: bool):
        self.choice = choice
        self.is_valid = is_valid


class ManageCharacterViewState(ManageCharacterState):
    def __init__(self, manage_character_scene: ManageCharacterScene):
        super().__init__(manage_character_scene)
        self.has_updated = False
        self.massage_queue = []

    def _parse_input(self):
        try:
            user_input = input().strip()
            choice = int(user_input)
            return ManageCharacterViewInput(choice, True)
        except ValueError:
            return ManageCharacterViewInput(-1, False)

    def handle_input(self):
        self.last_user_input = self._parse_input()

    def update(self):
        self.has_updated = True
        if self.last_user_input.is_valid:
            if self.last_user_input.choice == 1:
                self.manage_character_scene.game.change_scene(SceneTypes.RESTING_HUB)
            elif self.last_user_input.choice == 2:
                # TODO: Implement level up
                pass
            else:
                self.massage_queue.append("Invalid input. Please enter [1] or [2].")
        else:
            self.massage_queue.append("Invalid input. Please enter [1] or [2].")

    def _render_message_queue(self):
        for message in self.massage_queue:
            print(message)
        self.massage_queue = []

    def _render_character(self):
        hero = self.manage_character_scene.game.hero
        print(f"Name: {hero.name}")
        print(f"Level: {hero.description}")
        print(f"Attack: {hero.stats.attack}")
        print(f"Defense: {hero.stats.defense}")
        print(f"Focus: {hero.stats.focus}")

    def _render_ask_for_input(self):
        print("What would you like to do?")
        print("[1] Go back to hub")
        print("[2] Level up")
        print("Enter the number of your choice: ", end="")

    def _render_message_queue(self):
        for message in self.massage_queue:
            print(message)
        self.massage_queue = []

    def render(self):
        if not self.has_updated:
            self._render_character()
        self._render_message_queue()
        self._render_ask_for_input()
