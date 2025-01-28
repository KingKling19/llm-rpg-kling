from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llm_rpg.scenes.manage_character.manage_character_scene import (
        ManageCharacterScene,
    )


class ManageCharacterState(ABC):
    def __init__(self, manage_character_scene: ManageCharacterScene):
        self.manage_character_scene = manage_character_scene

    @abstractmethod
    def handle_input(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
