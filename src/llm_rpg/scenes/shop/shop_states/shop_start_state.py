from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.shop.shop_states.shop_buying_state import ShopBuyingState
from llm_rpg.scenes.shop.shop_states.shop_state import ShopState

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_scene import ShopScene


class ShopStartState(ShopState):
    def __init__(self, shop_scene: ShopScene):
        self.shop_scene = shop_scene

    def handle_input(self):
        _ = input()

    def update(self):
        self.shop_scene.change_state(ShopBuyingState(self.shop_scene))

    def render(self):
        print("Welcome to the shop!")
        print("Press ENTER to continue")
