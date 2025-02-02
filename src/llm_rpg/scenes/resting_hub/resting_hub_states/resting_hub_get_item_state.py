from __future__ import annotations


from typing import TYPE_CHECKING, List, Optional


from llm_rpg.objects.item import Item, TurtleShell, PoetryBook, AdrenalinePump
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


class RestingHubGetItemState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene
        self.message_queue = []
        self.last_user_navigation_input = UserNavigationInput(-1, True)
        self.items: List[Item] = self._initialize_items()
        self.selected_item: Optional[Item] = None
        self.is_replacing_item = False
        self.display_discovered_items = True
        self.display_current_items_to_drop = False
        self.display_state_transition_header = True

    def _initialize_items(self):
        return [TurtleShell(), PoetryBook(), AdrenalinePump()]

    def handle_input(self):
        if self.is_replacing_item:
            possible_choices = [0]
            for i in range(len(self.resting_hub_scene.game.hero.inventory.items)):
                possible_choices.append(i + 1)
            self.last_user_navigation_input = get_user_navigation_input(
                possible_choices
            )
        elif self.resting_hub_scene.game.hero.discovered_item:
            self.last_user_navigation_input = get_user_navigation_input([0, 1, 2, 3])

    def update(self):
        # reset display flags
        self.display_discovered_items = False
        self.display_current_items_to_drop = False
        self.display_state_transition_header = False
        if not self.resting_hub_scene.game.hero.discovered_item:
            self.resting_hub_scene.change_state(RestingHubStates.NAVIGATION)
        else:
            if self.last_user_navigation_input.is_valid:
                if self.is_replacing_item:
                    if self.last_user_navigation_input.choice == 0:
                        self.display_discovered_items = True
                    else:
                        item_to_remove = (
                            self.resting_hub_scene.game.hero.inventory.items[
                                self.last_user_navigation_input.choice - 1
                            ]
                        )
                        self.resting_hub_scene.game.hero.replace_item_with_discovered_item(
                            item_to_remove=item_to_remove,
                            discovered_item=self.chosen_item,
                        )
                        self.message_queue.append(
                            f"You have replaced your {item_to_remove.name} with a {self.chosen_item.name}."
                        )
                    self.is_replacing_item = False
                else:
                    if self.last_user_navigation_input.choice == 0:
                        self.resting_hub_scene.game.hero.dont_pick_up_item()
                    else:
                        self.chosen_item = self.items[
                            self.last_user_navigation_input.choice - 1
                        ]
                        if self.resting_hub_scene.game.hero.inventory.is_full():
                            self.is_replacing_item = True
                            self.display_current_items_to_drop = True
                        else:
                            self.resting_hub_scene.game.hero.pick_up_discovered_item(
                                self.chosen_item
                            )
                            self.message_queue.append(
                                f"You have received a {self.chosen_item.name}."
                            )

    def _display_current_items_to_drop(self):
        print(
            f"You have reached your limit of {self.resting_hub_scene.game.hero.inventory.max_items} items."
        )
        print(f"Which item do you want to replace with {self.chosen_item.name}?")
        for index, item in enumerate(self.resting_hub_scene.game.hero.inventory.items):
            print(f"[{index + 1}] {item.name}: {item.description}")
        print("")
        print("Or press:")
        print("[0] to cancel dropping items.")

    def _display_discovered_items(self):
        print("")
        print("The enemy has dropped some items.")
        print("Choose one item to pick up.")
        for index, item in enumerate(self.items):
            print(f"[{index + 1}] {item.name}: {item.description}")
        print("")
        print("Or press:")
        print("[0] to not pick up any item.")

    def _display_invalid_input(self):
        if self.is_replacing_item:
            total_choices = len(self.resting_hub_scene.game.hero.inventory.items) + 1
        else:
            total_choices = len(self.items) + 1
        base_string = "Invalid input: choose "
        for i in range(total_choices):
            base_string += f"[{i}]"
            if i < total_choices - 1:
                base_string += ", "
            else:
                base_string += "."
        self.message_queue.append(base_string)

    def _render_message_queue(self):
        for message in self.message_queue:
            print(message)
        self.message_queue = []

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header("Item Discovery")
        if self.display_discovered_items:
            self._display_discovered_items()
        elif self.display_current_items_to_drop:
            self._display_current_items_to_drop()
        elif not self.last_user_navigation_input.is_valid:
            self._display_invalid_input()
        self._render_message_queue()
