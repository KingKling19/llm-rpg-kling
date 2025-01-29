from __future__ import annotations
from llm_rpg.llm.llm import GroqLLM
from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from llm_rpg.objects.character import Stats
from llm_rpg.systems.hero.hero import Hero
from llm_rpg.systems.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_scene import BattleScene

from typing import TYPE_CHECKING
from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene
from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.systems.battle.enemy import Enemy

if TYPE_CHECKING:
    from llm_rpg.scenes.scene import Scene


class Game:
    def __init__(self):
        self.llm = GroqLLM(llm_cost_tracker=LLMCostTracker())
        self.is_running = True
        self.hero = Hero(
            name="Thalor",
            description="A fierce warrior with a mysterious past and unmatched swordsmanship",
            stats=Stats(level=5, attack=100, defense=10, focus=20, hp=30),
            items=[],
        )
        self.current_scene: Scene | None = self.get_resting_hub_scene()

    def get_battle_scene(self):
        enemy = Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            stats=Stats(level=5, attack=10, defense=10, focus=20, hp=30),
            llm=self.llm,
        )

        battle_ai = BattleAI(llm=self.llm)
        return BattleScene(self, self.hero, enemy, battle_ai)

    def get_resting_hub_scene(self):
        return RestingHubScene(self)

    def change_scene(self, scene_type: SceneTypes):
        if scene_type == SceneTypes.BATTLE:
            self.current_scene = self.get_battle_scene()
        elif scene_type == SceneTypes.RESTING_HUB:
            self.current_scene = self.get_resting_hub_scene()
        else:
            raise ValueError(f"Tried to change to invalid scene: {scene_type}")

    def run(self):
        # print initial scene
        self.current_scene.render()
        while self.is_running:
            self.current_scene.handle_input()
            self.current_scene.update()
            self.current_scene.render()

        print(f"Total llm cost $: {self.llm.llm_cost_tracker.total_cost}")
