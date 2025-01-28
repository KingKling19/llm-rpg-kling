from __future__ import annotations

from typing import TYPE_CHECKING
from llm_rpg.objects.item import CRYSTAL, SHIELD, SWORD
from llm_rpg.scenes.scene import Scene
from llm_rpg.scenes.shop.shop_states.shop_buying_state import ShopBuyingState


if TYPE_CHECKING:
    from llm_rpg.scenes.state import State
    from llm_rpg.game.game import Game


class ShopScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game)
        self.current_state: State = ShopBuyingState(self)
        self.items = self._init_items()

    def _init_items(self):
        return [SWORD, SHIELD, CRYSTAL]
