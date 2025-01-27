from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.shop.shop_states.shop_state import ShopState

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_scene import ShopScene


class ShopEndState(ShopState):
    def __init__(self, shop_scene: ShopScene):
        self.shop_scene = shop_scene

    def handle_input(self):
        _ = input()

    def update(self):
        self.shop_scene.game.is_running = False

    def render(self):
        print("Thank you for visiting the shop!")
        print("Press ENTER to continue")
