from __future__ import annotations

from typing import TYPE_CHECKING


from llm_rpg.scenes.battle.battle_states.battle_states import BattleStates

from llm_rpg.scenes.battle.battle_states.battle_end_state import BattleEndState
from llm_rpg.scenes.battle.battle_states.battle_start_state import BattleStartState
from llm_rpg.scenes.battle.battle_states.battle_turn_state import BattleTurnState
from llm_rpg.systems.hero.hero import Hero
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
        hero: Hero,
        enemy: Enemy,
        battle_ai: BattleAI,
    ):
        super().__init__(game=game, current_state=BattleStartState(self))
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker()
        self.damage_calculator = DamageCalculator()

    def change_state(self, new_state: BattleStates):
        if new_state == BattleStates.START:
            self.current_state = BattleStartState(self)
        elif new_state == BattleStates.TURN:
            self.current_state = BattleTurnState(self)
        elif new_state == BattleStates.END:
            self.current_state = BattleEndState(self)
