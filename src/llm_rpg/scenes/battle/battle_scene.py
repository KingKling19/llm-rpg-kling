from __future__ import annotations

from typing import TYPE_CHECKING


from llm_rpg.scenes.battle.battle_states.battle_states import BattleStates

from llm_rpg.scenes.battle.battle_states.battle_end_state import BattleEndState
from llm_rpg.scenes.battle.battle_states.battle_start_state import BattleStartState
from llm_rpg.scenes.battle.battle_states.battle_turn_state import BattleTurnState
from llm_rpg.systems.battle.battle_ai import BattleAI
from llm_rpg.systems.battle.battle_log import BattleLog

from llm_rpg.systems.battle.creativity_tracker import CreativityTracker
from llm_rpg.systems.battle.damage_calculator import (
    DamageCalculator,
)
from llm_rpg.scenes.scene import Scene
from llm_rpg.systems.battle.enemy import Enemy

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class BattleScene(Scene):
    def __init__(
        self,
        game: Game,
        enemy: Enemy,
    ):
        super().__init__(game=game, current_state=BattleStartState(self))
        self.hero = self.game.hero
        self.enemy = enemy
        self.battle_ai = BattleAI(llm=self.game.llm, debug=self.game.config.debug_mode)
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker(
            word_overuse_threshold=game.config.creativity_word_overuse_threshold
        )
        self.damage_calculator = DamageCalculator(game_config=game.config)

    def change_state(self, new_state: BattleStates):
        if new_state == BattleStates.START:
            self.current_state = BattleStartState(self)
        elif new_state == BattleStates.TURN:
            self.current_state = BattleTurnState(self)
        elif new_state == BattleStates.END:
            self.current_state = BattleEndState(self)
