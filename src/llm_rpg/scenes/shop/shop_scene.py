from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.objects.item import CRYSTAL, SHIELD, SWORD
from llm_rpg.scenes.scene import Scene
from llm_rpg.scenes.shop.shop_states.shop_start_state import ShopStartState

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_states.shop_state import ShopState
    from llm_rpg.game.game import Game


class ShopScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.current_state: ShopState = ShopStartState(self)
        self.items = self._init_items()

    def _init_items(self):
        return [SWORD, SHIELD, CRYSTAL]

    def change_state(self, new_state: ShopState):
        self.current_state = new_state

    def handle_input(self):
        self.current_state.handle_input()

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
