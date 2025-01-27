from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.shop.shop_states.shop_end_state import ShopEndState
from llm_rpg.scenes.shop.shop_states.shop_state import ShopState

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_scene import ShopScene


class UserShopInput:
    def __init__(self, try_to_buy_item: int, wants_to_leave_shop: bool, valid: bool):
        self.try_to_buy_item = try_to_buy_item
        self.wants_to_leave_shop = wants_to_leave_shop
        self.valid = valid


class ShopBuyingState(ShopState):
    def __init__(self, shop_scene: ShopScene):
        self.shop_scene = shop_scene
        self.last_user_shop_input = UserShopInput(
            try_to_buy_item=-1, wants_to_leave_shop=False, valid=False
        )
        self.message_queue: list[str] = []
        self.has_updated = False
        self.purchased_new_item = False

    def _parse_user_shop_input(self):
        try:
            user_input = input().strip()
            if user_input == "leave":
                return UserShopInput(
                    try_to_buy_item=-1, wants_to_leave_shop=True, valid=True
                )
            valid_user_inputs = [i for i in range(1, len(self.shop_scene.items) + 1)]
            item_index = int(user_input)
            if item_index not in valid_user_inputs:
                raise ValueError
            return UserShopInput(
                try_to_buy_item=item_index, wants_to_leave_shop=False, valid=True
            )
        except ValueError:
            return UserShopInput(
                try_to_buy_item=-1, wants_to_leave_shop=False, valid=False
            )

    def handle_input(self):
        self.last_user_shop_input = self._parse_user_shop_input()

    def update(self):
        self.has_updated = True
        self.purchased_new_item = False
        if self.last_user_shop_input.valid:
            if self.last_user_shop_input.wants_to_leave_shop:
                self.shop_scene.change_state(ShopEndState(self.shop_scene))
            else:
                if (
                    self.shop_scene.game.hero.gold
                    < self.shop_scene.items[
                        self.last_user_shop_input.try_to_buy_item - 1
                    ].cost
                ):
                    self.message_queue.append("You don't have enough gold!")
                else:
                    self.shop_scene.game.hero.gold -= self.shop_scene.items[
                        self.last_user_shop_input.try_to_buy_item - 1
                    ].cost
                    self.shop_scene.game.hero.items.append(
                        self.shop_scene.items[
                            self.last_user_shop_input.try_to_buy_item - 1
                        ]
                    )
                    self.purchased_new_item = True
                    self.message_queue.append(
                        f"You bought the following item: {self.shop_scene.items[self.last_user_shop_input.try_to_buy_item - 1].name}"
                    )
                    self.shop_scene.items.pop(
                        self.last_user_shop_input.try_to_buy_item - 1
                    )
        else:
            self.message_queue.append("Invalid input.")

    def _render_current_gold(self):
        print(f"You have {self.shop_scene.game.hero.gold} gold.")

    def _render_message_queue(self):
        if self.message_queue:
            for message in self.message_queue:
                print(message)
            self.message_queue = []

    def _render_items_in_shop(self):
        print("The shop offers the following items:")
        print("-" * 50)
        for i, item in enumerate(self.shop_scene.items, 1):
            print(f"[{i}] {item.name} (Rarity: {item.rarity})")
            print(f"    Description: {item.description}")
            print(f"    Cost: {item.cost} gold")
            print("-" * 50)

    def _render_ask_user_to_buy_item(self):
        print("\nWhat would you like to do?")
        print(
            "- To buy an item: Enter its number (1-{})".format(
                len(self.shop_scene.items)
            )
        )
        print("- To exit shop: Type 'leave'")
        print("\nYour choice: ", end="")

    def render(self):
        if not self.has_updated:
            self._render_current_gold()
            self._render_items_in_shop()
            self._render_message_queue()
        else:
            self._render_message_queue()
            if self.purchased_new_item:
                self._render_current_gold()
                self._render_items_in_shop()
        self._render_ask_user_to_buy_item()
