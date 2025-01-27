from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llm_rpg.scenes.shop.shop_scene import ShopScene


class ShopState(ABC):
    def __init__(self, shop_scene: ShopScene):
        self.shop_scene = shop_scene

    @abstractmethod
    def handle_input(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
