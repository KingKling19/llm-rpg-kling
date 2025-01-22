from __future__ import annotations
from llm_rpg.llm.llm import GroqLLM
from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from llm_rpg.objects.character import Enemy, Hero, Stats
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_scene import BattleScene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llm_rpg.scenes.scene import Scene


class Game:
    def __init__(self):

        self.llm = GroqLLM(
            llm_cost_tracker=LLMCostTracker(),
        )
        self.current_scene: Scene | None = self.get_initial_scene()
        self.is_running = True

    def get_initial_scene(self):
        hero = Hero(
            name="Thalor",
            description="A fierce warrior with a mysterious past and unmatched swordsmanship",
            stats=Stats(level=5, attack=10, defense=10, focus=20, hp=30),
        )
        enemy = Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            stats=Stats(level=5, attack=10, defense=10, focus=20, hp=30),
            llm=self.llm,
        )

        battle_ai = BattleAI(llm=self.llm)
        return BattleScene(self, hero, enemy, battle_ai)

    def change_scene(self, scene_name: str):
        self.current_scene = self.scenes[scene_name]

    def run(self):
        # print initial scene
        self.current_scene.render()
        while self.is_running:
            self.current_scene.handle_input()
            self.current_scene.update()
            self.current_scene.render()

        print(f"Total llm cost $: {self.llm.llm_cost_tracker.total_cost}")
