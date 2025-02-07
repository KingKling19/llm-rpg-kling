from __future__ import annotations


from llm_rpg.scenes.main_menu.main_menu_states.main_menu_states import MainMenuStates
from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State

from typing import TYPE_CHECKING

from llm_rpg.utils.user_navigation_input import (
    UserNavigationInput,
    get_user_navigation_input,
)

if TYPE_CHECKING:
    from llm_rpg.scenes.main_menu.main_menu_scene import MainMenuScene


class MainMenuNavigationState(State):
    def __init__(self, scene: MainMenuScene):
        self.scene = scene
        self.display_state_transition_header = True
        self.display_title_screen = True
        self.last_user_navigation_input: UserNavigationInput | None = None

    def handle_input(self):
        self.last_user_navigation_input = get_user_navigation_input([1, 2])

    def update(self):
        self.display_info = False
        self.display_state_transition_header = False
        if self.last_user_navigation_input.is_valid:
            if self.last_user_navigation_input.choice == 1:
                self.scene.game.change_scene(SceneTypes.HERO_CREATION)
            elif self.last_user_navigation_input.choice == 2:
                self.scene.change_state(MainMenuStates.INFO)

    def _render_title_screen(self):
        print(
            """


 ▄█        ▄█         ▄▄▄▄███▄▄▄▄           ▄████████    ▄███████▄    ▄██████▄  
███       ███       ▄██▀▀▀███▀▀▀██▄        ███    ███   ███    ███   ███    ███ 
███       ███       ███   ███   ███        ███    ███   ███    ███   ███    █▀  
███       ███       ███   ███   ███       ▄███▄▄▄▄██▀   ███    ███  ▄███        
███       ███       ███   ███   ███      ▀▀███▀▀▀▀▀   ▀█████████▀  ▀▀███ ████▄  
███       ███       ███   ███   ███      ▀███████████   ███          ███    ███ 
███▌    ▄ ███▌    ▄ ███   ███   ███        ███    ███   ███          ███    ███ 
█████▄▄██ █████▄▄██  ▀█   ███   █▀         ███    ███  ▄████▀        ████████▀  
▀         ▀                                ███    ███                           
"""
        )
        print("Choose an option:")
        print("[1] Start New Game")
        print("[2] Info")

    def _render_invalid_choice(self):
        print("Invalid choice. Choose [1] or [2]")

    def render(self):
        if self.display_title_screen:
            self._render_title_screen()
        if (
            self.last_user_navigation_input
            and not self.last_user_navigation_input.is_valid
        ):
            self._render_invalid_choice()
