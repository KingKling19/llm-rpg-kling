from __future__ import annotations
from llm_rpg.game.game_config import GameConfig
from llm_rpg.llm.llm import GroqLLM
from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from llm_rpg.scenes.factory import SceneFactory
from llm_rpg.systems.hero.hero import Hero

from typing import TYPE_CHECKING
from llm_rpg.scenes.scene import SceneTypes

if TYPE_CHECKING:
    from llm_rpg.scenes.scene import Scene


class Game:
    def __init__(self, config: GameConfig):
        self.config = config
        self.llm = GroqLLM(
            llm_cost_tracker=LLMCostTracker(), model=self.config.llm_model
        )
        self.is_running = True
        self.hero = Hero(
            name="",
            description="",
            level=1,
            base_stats=self.config.hero_base_stats,
        )
        self.scene_factory = SceneFactory(self)
        self.current_scene: Scene = self.scene_factory.get_hero_creation_scene()
        self.battles_won = 0

    def change_scene(self, scene_type: SceneTypes):
        if scene_type == SceneTypes.BATTLE:
            self.current_scene = self.scene_factory.get_battle_scene()
        elif scene_type == SceneTypes.RESTING_HUB:
            self.current_scene = self.scene_factory.get_resting_hub_scene()
        elif scene_type == SceneTypes.HERO_CREATION:
            self.current_scene = self.scene_factory.get_hero_creation_scene()
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
