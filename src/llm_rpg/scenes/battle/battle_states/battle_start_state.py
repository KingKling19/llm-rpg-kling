from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.battle.battle_states.battle_states import BattleStates
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleStartState(State):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene

    def handle_input(self):
        pass

    def update(self):
        self.battle_scene.change_state(BattleStates.TURN)

    def _render_battle_number(self):
        print(f"Battle {self.battle_scene.game.battles_won + 1}")

    def render(self):
        self._render_battle_number()
        self.battle_scene.hero.render()
        self.battle_scene.enemy.render()
