from __future__ import annotations
import random
from typing import TYPE_CHECKING

from llm_rpg.objects.character import StatTypes, Stats
from llm_rpg.scenes.battle.battle_scene import BattleScene
from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene
from llm_rpg.systems.battle.battle_ai import BattleAI
from llm_rpg.systems.battle.difficulty_scaling import scale_enemy
from llm_rpg.systems.battle.enemy import Enemy, EnemyArchetypes

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class SceneFactory:
    def __init__(self, game: Game):
        self.game = game

    def _get_enemy(self) -> Enemy:
        enemy = Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            level=1,
            base_stats=Stats(attack=10, defense=10, focus=20, max_hp=10),
            llm=self.game.llm,
            archetype=EnemyArchetypes.ATTACKER,
        )

        scale_enemy(enemy=enemy, battles_won=20)

        return enemy

    def get_battle_scene(self) -> BattleScene:
        enemy = self._get_enemy()

        battle_ai = BattleAI(llm=self.game.llm)
        return BattleScene(
            game=self.game, hero=self.game.hero, enemy=enemy, battle_ai=battle_ai
        )

    def get_resting_hub_scene(self) -> RestingHubScene:
        return RestingHubScene(game=self.game)
