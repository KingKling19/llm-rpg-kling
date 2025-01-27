from __future__ import annotations

from llm_rpg.scenes.battle.battle_states.battle_state import BattleState
from typing import TYPE_CHECKING

from llm_rpg.scenes.scene import SceneTypes

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleEndState(BattleState):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene

    def handle_input(self):
        pass

    def update(self):
        self.battle_scene.game.change_scene(SceneTypes.SHOP)

    def _render_character_stats(self):
        print(
            f"{self.battle_scene.hero.name} HP: {self.battle_scene.hero.stats.hp}/{self.battle_scene.hero.stats.max_hp} Focus: {self.battle_scene.hero.stats.focus}/{self.battle_scene.hero.stats.max_focus}"
        )
        print(
            f"{self.battle_scene.enemy.name} HP: {self.battle_scene.enemy.stats.hp}/{self.battle_scene.enemy.stats.max_hp}"
        )

    def render(self):
        if self.battle_scene.battle_log.events:
            print("")
            print("--- The following events took place... --- \n")
            string_of_last_2_events = (
                self.battle_scene.battle_log.get_string_of_last_2_events()
            )
            print(string_of_last_2_events)
        print("--- Current Stats --- \n")
        self._render_character_stats()
        print("")
        print("Game Ended")
        if self.battle_scene.hero.stats.hp > 0:
            print(f"{self.battle_scene.hero.name} won!")
        else:
            print(f"{self.battle_scene.enemy.name} won!")
