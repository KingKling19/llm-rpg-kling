from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.objects.item import TurtleShell, PoetryBook, AdrenalinePump
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


class RestingHubGetItemState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.has_updated = False
        self.message_queue = []
        self.last_user_navigation_input = UserNavigationInput(-1, False)
        self.items = self._initialize_items()

    def _initialize_items(self):
        return [TurtleShell(), PoetryBook(), AdrenalinePump()]

    def handle_input(self):
        if not self.has_updated:
            self.last_user_navigation_input = get_user_navigation_input([1, 2, 3])

    def update(self):
        self.has_updated = True
        if not self.resting_hub_scene.game.hero.discovered_item:
            self.resting_hub_scene.change_state(RestingHubStates.NAVIGATION)
        else:
            if self.last_user_navigation_input.is_valid:
                chosen_item = self.items[self.last_user_navigation_input.choice - 1]
                if self.last_user_navigation_input.choice == 1:
                    self.resting_hub_scene.game.hero.inventory.add_item(chosen_item)
                    self.message_queue.append(
                        f"You have received a {chosen_item.name}."
                    )
                elif self.last_user_navigation_input.choice == 2:
                    self.resting_hub_scene.game.hero.inventory.add_item(chosen_item)
                    self.message_queue.append(
                        f"You have received a {chosen_item.name}."
                    )
                elif self.last_user_navigation_input.choice == 3:
                    self.resting_hub_scene.game.hero.inventory.add_item(chosen_item)
                    self.message_queue.append(
                        f"You have received a {chosen_item.name}."
                    )
                self.resting_hub_scene.game.hero.discovered_item = False
            else:
                self.message_queue.append(
                    "Invalid input. Please enter [1] or [2] or [3]."
                )

    def _display_items(self):
        print("")
        print("The enemy has dropped some items.")
        print("Choose one item to pick up.")
        print(f"[1] {self.items[0].name}: {self.items[0].description}")
        print(f"[2] {self.items[1].name}: {self.items[1].description}")
        print(f"[3] {self.items[2].name}: {self.items[2].description}")

    def _render_message_queue(self):
        for message in self.message_queue:
            print(message)
        self.message_queue = []

    def render(self):
        if not self.has_updated:
            self._display_items()
        self._render_message_queue()
