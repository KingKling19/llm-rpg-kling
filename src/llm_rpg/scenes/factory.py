from __future__ import annotations
import random
from typing import TYPE_CHECKING

from llm_rpg.objects.character import Stats
from llm_rpg.scenes.battle.battle_scene import BattleScene
from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene
from llm_rpg.systems.battle.battle_ai import BattleAI
from llm_rpg.systems.battle.enemy import Enemy

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class SceneFactory:
    def __init__(self, game: Game):
        self.game = game

    def _get_enemy(self) -> Enemy:
        generated_stats = Stats(attack=10, defense=10, focus=20, hp=10)
        enemy_gain_levels = self.game.battles_won
        for _ in range(enemy_gain_levels):
            stat_index = random.randint(0, 2)
            if stat_index == 0:
                generated_stats.attack += 5
            elif stat_index == 1:
                generated_stats.defense += 5
            elif stat_index == 2:
                generated_stats.hp += 5
                generated_stats.max_hp += 5

        return Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            level=enemy_gain_levels + 1,
            stats=generated_stats,
            llm=self.game.llm,
        )

    def get_battle_scene(self) -> BattleScene:
        enemy = self._get_enemy()

        battle_ai = BattleAI(llm=self.game.llm)
        return BattleScene(
            game=self.game, hero=self.game.hero, enemy=enemy, battle_ai=battle_ai
        )

    def get_resting_hub_scene(self) -> RestingHubScene:
        return RestingHubScene(game=self.game)
