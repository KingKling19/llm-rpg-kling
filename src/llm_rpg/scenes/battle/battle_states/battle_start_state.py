from __future__ import annotations


from typing import TYPE_CHECKING

from llm_rpg.scenes.battle.battle_states.battle_turn_state import BattleTurnState
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleStartState(State):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene

    def handle_input(self):
        _ = input()

    def update(self):
        self.battle_scene.change_state(BattleTurnState(self.battle_scene))

    def render(self):
        self.battle_scene.hero.render()
        self.battle_scene.enemy.render()
        print("Press Enter to start the battle")
