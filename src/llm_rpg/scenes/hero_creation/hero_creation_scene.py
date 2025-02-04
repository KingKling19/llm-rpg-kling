from __future__ import annotations

from typing import TYPE_CHECKING

from llm_rpg.scenes.hero_creation.hero_creation_states.hero_creation_choose_class_state import (
    HeroCreationChooseClassState,
)
from llm_rpg.scenes.hero_creation.hero_creation_states.hero_creation_choose_name_state import (
    HeroCreationChooseNameState,
)
from llm_rpg.scenes.hero_creation.hero_creation_states.hero_creation_states import (
    HeroCreationStates,
)
from llm_rpg.scenes.scene import Scene


if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class HeroCreationScene(Scene):
    def __init__(self, game: Game):
        super().__init__(game=game)
        self.current_state = HeroCreationChooseNameState(self)

    def change_state(self, new_state: HeroCreationStates):
        if new_state == HeroCreationStates.CHOOSE_CLASS:
            self.current_state = HeroCreationChooseClassState(self)
        elif new_state == HeroCreationStates.CHOOSE_NAME:
            self.current_state = HeroCreationChooseNameState(self)
        else:
            raise ValueError(f"Invalid state: {new_state}")
