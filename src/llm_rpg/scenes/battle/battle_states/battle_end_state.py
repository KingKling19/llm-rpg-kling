from __future__ import annotations

from typing import TYPE_CHECKING

from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleEndState(State):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene

    def handle_input(self):
        pass

    def update(self):
        if not self.battle_scene.hero.is_dead():
            self.battle_scene.game.battles_won += 1
            if self.battle_scene.game.battles_won % 2 == 0:
                self.battle_scene.hero.discovered_item = True
            if self.battle_scene.game.battles_won % 3 == 0:
                self.battle_scene.hero.should_level_up = True
            self.battle_scene.hero.full_heal()
            self.battle_scene.game.change_scene(SceneTypes.RESTING_HUB)
        else:
            self.battle_scene.game.change_scene(SceneTypes.GAME_OVER)

    def _render_character_stats(self):
        print(
            f"{self.battle_scene.hero.name} HP: {self.battle_scene.hero.hp}/{self.battle_scene.hero.get_current_stats().max_hp}"
        )
        print(
            f"{self.battle_scene.enemy.name} HP: {self.battle_scene.enemy.hp}/{self.battle_scene.enemy.get_current_stats().max_hp}"
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
        if not self.battle_scene.hero.is_dead():
            print(f"{self.battle_scene.hero.name} won!")
        else:
            print(f"{self.battle_scene.enemy.name} won!")
