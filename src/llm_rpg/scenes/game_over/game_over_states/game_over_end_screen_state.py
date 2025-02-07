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
    from llm_rpg.scenes.game_over.game_over_scene import GameOverScene


class GameOverEndScreenState(State):
    def __init__(self, scene: GameOverScene):
        self.scene = scene
        self.display_state_transition_header = True
        self.display_end_screen = True
        self.last_user_navigation_input: UserNavigationInput | None = None

    def handle_input(self):
        self.last_user_navigation_input = get_user_navigation_input([1, 2])

    def update(self):
        self.display_end_screen = False
        self.display_state_transition_header = False
        if self.last_user_navigation_input.is_valid:
            if self.last_user_navigation_input.choice == 1:
                self.scene.game.change_scene(SceneTypes.MAIN_MENU)
            elif self.last_user_navigation_input.choice == 2:
                self.scene.game.is_running = False

    def _render_game_over_screen(self):
        print(
            """

   ▄██████▄     ▄████████   ▄▄▄▄███▄▄▄▄      ▄████████      ▄██████▄   ▄█    █▄     ▄████████    ▄████████ 
  ███    ███   ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███     ███    ███ ███    ███   ███    ███   ███    ███ 
  ███    █▀    ███    ███ ███   ███   ███   ███    █▀      ███    ███ ███    ███   ███    █▀    ███    ███ 
 ▄███          ███    ███ ███   ███   ███  ▄███▄▄▄         ███    ███ ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███ ████▄  ▀███████████ ███   ███   ███ ▀▀███▀▀▀         ███    ███ ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███    ███   ███    ███ ███   ███   ███   ███    █▄      ███    ███ ███    ███   ███    █▄  ▀███████████ 
  ███    ███   ███    ███ ███   ███   ███   ███    ███     ███    ███ ███    ███   ███    ███   ███    ███ 
  ████████▀    ███    █▀   ▀█   ███   █▀    ██████████      ▀██████▀   ▀██████▀    ██████████   ███    ███ 
                                                                                                ███    ███ 

"""
        )
        print("You have been defeated by the enemy.")
        print("Please select an option:\n")
        print("[1] Go to main menu")
        print("[2] Exit game")

    def _render_invalid_choice(self):
        print("Invalid choice. Choose [1] or [2]:")

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header(
                "Game Over",
            )
        if self.display_end_screen:
            self._render_game_over_screen()
        if (
            self.last_user_navigation_input
            and not self.last_user_navigation_input.is_valid
        ):
            self._render_invalid_choice()
