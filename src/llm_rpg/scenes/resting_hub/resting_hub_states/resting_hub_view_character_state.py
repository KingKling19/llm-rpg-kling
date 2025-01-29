from __future__ import annotations


from typing import TYPE_CHECKING


from llm_rpg.scenes.scene import SceneTypes
from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.resting_hub.resting_hub_scene import RestingHubScene


class RestingHubViewCharacterState(State):
    def __init__(self, resting_hub_scene: RestingHubScene):
        self.resting_hub_scene = resting_hub_scene

    def handle_input(self):
        pass

    def update(self):
        self.resting_hub_scene.game.change_scene(SceneTypes.RESTING_HUB)

    def _render_character(self):
        hero = self.resting_hub_scene.game.hero
        print(f"Name: {hero.name}")
        print(f"Level: {hero.description}")
        print(f"Attack: {hero.stats.attack}")
        print(f"Defense: {hero.stats.defense}")
        print(f"Focus: {hero.stats.focus}")

    def render(self):
        self._render_character()
