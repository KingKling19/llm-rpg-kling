from math import ceil
import random
import time

from llm_rpg.objects.character import Hero, Enemy
from llm_rpg.llm.llm import LLM
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_log import BattleEvent, BattleLog
from llm_rpg.utils.timer import Timer


class Battle:
    def __init__(self, hero: Hero, enemy: Enemy, battle_ai: BattleAI):
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()

    def hero_turn(self):
        with Timer() as timer:
            proposed_action = self.hero.get_next_action()
        print(f"Hero turn took: {timer.interval:.2f} seconds")
        print("\n=== HERO TURN ===")
        print(f"🦸 tries to: {proposed_action}")

        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_action,
            attacking_character=self.hero,
            defending_character=self.enemy,
            battle_log_string=self.battle_log.to_string(),
        )

        print(f"⚡ Effect: {action_effect.effect_description}")
        print(f"  - feasibility: {action_effect.feasibility}")
        print(f"  - potential_damage: {action_effect.potential_damage}")

        self.battle_log.add_action(
            BattleEvent(
                character_name=self.hero.name,
                proposed_action=proposed_action,
                effect_description=action_effect.effect_description,
            )
        )

        damage = self._calculate_damage(
            attack=self.hero.stats.attack,
            defense=self.enemy.stats.defense,
            feasibility=action_effect.feasibility,
            potential_damage=action_effect.potential_damage,
        )

        print(f"💥 Damage dealt: {damage:.0f}")
        self.enemy.stats.hp -= damage
        print(f"❤️  Enemy HP: {self.enemy.stats.hp:.1f}/{self.enemy.stats.max_hp:.1f}\n")

    def enemy_turn(self):
        proposed_enemy_action = self.enemy.get_next_action(self.battle_log, self.hero)

        print("\n=== ENEMY TURN ===")
        print(f"👾 tries to: {proposed_enemy_action}")

        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_enemy_action,
            attacking_character=self.enemy,
            defending_character=self.hero,
            battle_log_string=self.battle_log.to_string(),
        )

        print(f"⚡ Effect: {action_effect.effect_description}")
        print(f"  - feasibility: {action_effect.feasibility}")
        print(f"  - potential_damage: {action_effect.potential_damage}")

        self.battle_log.add_action(
            BattleEvent(
                character_name=self.enemy.name,
                proposed_action=proposed_enemy_action,
                effect_description=action_effect.effect_description,
            )
        )

        damage = self._calculate_damage(
            attack=self.enemy.stats.attack,
            defense=self.hero.stats.defense,
            feasibility=action_effect.feasibility,
            potential_damage=action_effect.potential_damage,
        )
        print(f"💥 Damage dealt: {damage:.0f}")
        self.hero.stats.hp -= damage
        print(f"❤️  Hero HP: {self.hero.stats.hp:.1f}/{self.hero.stats.max_hp:.1f}\n")

    def _calculate_damage(
        self, attack: int, defense: int, feasibility: float, potential_damage: float
    ) -> int:
        # base dmg depends purely on attack, defense and a random factor
        random_factor = random.uniform(0.95, 1.05)
        base_dmg = (attack / 2 - defense / 4) * random_factor
        if base_dmg <= 0:
            base_dmg = 1

        # total dmg depends on the action feasibility and potential damage which are
        # determined by the LLM
        EFFECTIVENESS_DMG_SCALING = 2
        total_dmg = (
            base_dmg * EFFECTIVENESS_DMG_SCALING * feasibility * potential_damage
        )

        return ceil(total_dmg)

    def start(self):
        print(f"The Battle has started! {self.hero.name} vs {self.enemy.name}")
        self.advance_turn()

    def advance_turn(self):
        self.hero_turn()
        if self.enemy.stats.hp <= 0:
            print(f"{self.enemy.name} is dead!")
            return
        self.enemy_turn()
        if self.hero.stats.hp <= 0:
            print(f"{self.hero.name} is dead!")
            return
        self.advance_turn()
