from __future__ import annotations

from typing import TYPE_CHECKING

from llm_rpg.objects.character import Enemy, Hero
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_log import BattleLog

from llm_rpg.scenes.battle.creativity_tracker import CreativityTracker
from llm_rpg.scenes.battle.damage_calculator import (
    DamageCalculator,
)
from llm_rpg.scenes.scene import Scene
from llm_rpg.scenes.battle.battle_states.battle_start_state import BattleStartState

if TYPE_CHECKING:
    from llm_rpg.game.game import Game
    from llm_rpg.scenes.battle.battle_states.battle_turn_state import BattleState


class BattleScene(Scene):
    def __init__(
        self,
        game: Game,
        hero: Hero,
        enemy: Enemy,
        battle_ai: BattleAI,
    ):
        super().__init__(game)
        self.current_state: BattleState = BattleStartState(self)
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker()
        self.damage_calculator = DamageCalculator()

    def change_state(self, new_state: BattleState):
        self.current_state = new_state

    def handle_input(self):
        self.current_state.handle_input()

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
