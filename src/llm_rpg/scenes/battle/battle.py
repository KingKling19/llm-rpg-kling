import random

from llm_rpg.objects.character import Hero, Enemy
from llm_rpg.llm.llm import LLM
from llm_rpg.scenes.battle.battle_log import BattleAction, BattleLog


class Battle:
    def __init__(self, hero: Hero, enemy: Enemy, llm: LLM):
        self.hero = hero
        self.enemy = enemy
        self.llm = llm
        self.battle_log = BattleLog()

    def determine_action_effectiveness(self, action: str, hero_turn: bool) -> float:
        is_valid_effect = False
        effect = 0
        attempts = 0
        while not is_valid_effect and attempts < 3:
            if hero_turn:
                character_a_description = self.hero.description
                character_b_description = self.enemy.description
            else:
                character_a_description = self.enemy.description
                character_b_description = self.hero.description

            prompt = f"""
                You are a video game ai that determines the attack effectiveness.
                Character A is attacking Character B.

                Based on the action and Character A and Character B's description, determine the attack effectiveness.

                The attack effectiveness is a number between 0 and 10.
                Where 0 is no effect at all and 10 is the maximum effect.

                Give as output only the number, nothing else.
                
                Character A description:
                {character_a_description}

                Character B description:
                {character_b_description}

                Action of character A:
                {action}
            """

            raw_output = self.llm.generate_completion(prompt)
            parsed_output = float(raw_output)
            if parsed_output < 0 or parsed_output > 10:
                attempts += 1
            else:
                is_valid_effect = True
                effect = parsed_output

        if not is_valid_effect:
            raise ValueError("Failed to determine attack effectiveness")

        return effect / 10

    def hero_turn(self):
        next_user_action = self.hero.get_next_action()
        self.battle_log.add_action(
            BattleAction(user="hero", action_description=next_user_action)
        )
        output = {
            "action": "hero_action",
            "description": f"Hero tries to: {next_user_action}",
        }
        print("\n=== HERO TURN ===")
        print(f"🦸 {output['description']}")
        action_effect = self.determine_action_effectiveness(
            action=next_user_action, hero_turn=True
        )
        print(f"⚡ Effectiveness: {action_effect:.2f}")
        damage = self._calculate_damage(
            attack=self.hero.stats.attack,
            defense=self.enemy.stats.defense,
            effectiveness=action_effect,
        )
        print(f"💥 Damage dealt: {damage:.0f}")
        output["enemy_hp_before"] = self.enemy.stats.hp
        self.enemy.stats.hp -= damage
        output["enemy_hp_after"] = self.enemy.stats.hp
        print(f"❤️  Enemy HP: {self.enemy.stats.hp:.1f}/{self.enemy.stats.max_hp:.1f}\n")

    def enemy_turn(self):
        enemy_action = self.enemy.get_next_action(self.battle_log, self.hero)
        self.battle_log.add_action(
            BattleAction(user="enemy", action_description=enemy_action)
        )
        output = {
            "action": "enemy_action",
            "description": f"Enemy action: {enemy_action}",
        }
        print("\n=== ENEMY TURN ===")
        print(f"👾 {output['description']}")
        action_effect = self.determine_action_effectiveness(
            action=enemy_action, hero_turn=False
        )
        print(f"⚡ Effectiveness: {action_effect:.2f}")
        damage = self._calculate_damage(
            attack=self.enemy.stats.attack,
            defense=self.hero.stats.defense,
            effectiveness=action_effect,
        )
        print(f"💥 Damage dealt: {damage:.0f}")
        output["hero_hp_before"] = self.hero.stats.hp
        self.hero.stats.hp -= damage
        output["hero_hp_after"] = self.hero.stats.hp
        print(f"❤️  Hero HP: {self.hero.stats.hp:.1f}/{self.hero.stats.max_hp:.1f}\n")

    def _calculate_damage(self, attack: int, defense: int, effectiveness: int) -> int:
        random_factor = random.uniform(0.95, 1.05)
        print(f"🎲 Random factor: {random_factor:.2f}")
        base_dmg = (attack / 2 - defense / 4) * random_factor
        EFFECTIVENESS_DMG_SCALING = 2
        total_dmg = base_dmg * EFFECTIVENESS_DMG_SCALING * effectiveness
        if total_dmg <= 0:
            total_dmg = 1
        return round(total_dmg)

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
