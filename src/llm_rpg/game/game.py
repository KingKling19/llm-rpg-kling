from llm_rpg.graphics.renderer import Renderer
from llm_rpg.llm.llm import GroqLLM
from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from llm_rpg.objects.character import Hero, Enemy, Stats
from llm_rpg.scenes.battle.battle import Battle
from llm_rpg.scenes.battle.battle_ai import BattleAI


def get_early_game_battle():
    llm = GroqLLM(
        llm_cost_tracker=LLMCostTracker(),
    )
    return Battle(
        hero=Hero(
            name="Thalor",
            description="A fierce warrior with a mysterious past and unmatched swordsmanship",
            stats=Stats(level=5, attack=10, defense=10, focus=20, hp=30),
        ),
        enemy=Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            stats=Stats(level=5, attack=10, defense=10, focus=20, hp=30),
            llm=llm,
        ),
        battle_ai=BattleAI(llm=llm),
        renderer=Renderer(llm=llm),
    )


def get_mid_game_battle():
    llm = GroqLLM(
        llm_cost_tracker=LLMCostTracker(),
    )
    return Battle(
        hero=Hero(
            name="Thalor",
            description="A fierce warrior with a mysterious past and unmatched swordsmanship",
            stats=Stats(level=10, attack=25, defense=25, focus=20, hp=30),
        ),
        enemy=Enemy(
            name="Zephyros",
            description="A cunning and ancient dragon with scales that shimmer like the night sky",
            stats=Stats(level=11, attack=30, defense=20, focus=20, hp=30),
            llm=llm,
        ),
        battle_ai=BattleAI(llm=llm),
        renderer=Renderer(llm=llm),
    )


class Game:
    def __init__(self):
        pass

    def start(self):
        battle = get_mid_game_battle()
        battle.start()
        print("--- Cost Analysis ---")
        battle.llm.llm_cost_tracker.display_costs()
