from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.shop.shop_states.shop_state import ShopState

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_scene import ShopScene


class ShopBuyingState(ShopState):
    def __init__(self, shop_scene: ShopScene):
        self.shop_scene = shop_scene

    def handle_input(self):
        _ = input()

    def update(self):
        pass

    def render(self):
        print("Buying")
