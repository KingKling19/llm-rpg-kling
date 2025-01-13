from llm_rpg.llm.llm import GroqLLM
from llm_rpg.llm.llm_cost_tracker import LLMCostTracker
from llm_rpg.objects.character import Hero, Enemy, Stats
from llm_rpg.scenes.battle.battle import Battle
from llm_rpg.scenes.battle.battle_ai import BattleAI


class Game:
    def __init__(self):
        pass

    def start(self):
        llm = GroqLLM(
            llm_cost_tracker=LLMCostTracker(),
        )
        print("Game Started")
        hero = Hero(
            name="Wout",
            description="Warrior with a sword",
            stats=Stats(attack=10, defense=10, focus=20, hp=30),
        )
        enemy = Enemy(
            name="Sparky",
            description="An ancient dragon",
            stats=Stats(attack=10, defense=10, focus=20, hp=30),
            llm=llm,
        )
        battle = Battle(
            hero=hero,
            enemy=enemy,
            battle_ai=BattleAI(llm=llm),
        )
        battle.start()
        print("--- Cost Analysis ---")
        llm.llm_cost_tracker.display_costs()
