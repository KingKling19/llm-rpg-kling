from llm_rpg.graphics.renderer import Renderer
from llm_rpg.objects.character import Hero, Enemy
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_log import BattleEvent, BattleLog
from llm_rpg.scenes.battle.creativity_tracker import CreativityTracker
from llm_rpg.scenes.battle.damage_calculator import DamageCalculator
from llm_rpg.utils.timer import Timer


class Battle:
    def __init__(
        self, hero: Hero, enemy: Enemy, battle_ai: BattleAI, renderer: Renderer
    ):
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker()
        self.damage_calculator = DamageCalculator()
        self.renderer = renderer

    def hero_turn(self):
        with Timer() as timer:
            proposed_action = self.hero.get_next_action()

        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_action,
            attacking_character=self.hero,
            defending_character=self.enemy,
            battle_log_string=self.battle_log.to_string(),
        )

        self.battle_log.add_action(
            BattleEvent(
                character_name=self.hero.name,
                proposed_action=proposed_action,
                effect_description=action_effect.effect_description,
            )
        )

        n_new_words_in_action = self.creativity_tracker.count_new_words_in_action(
            action=proposed_action
        )

        n_overused_words_in_action = (
            self.creativity_tracker.count_overused_words_in_action(
                action=proposed_action
            )
        )

        damage_calculation_result = self.damage_calculator.calculate_damage(
            attack=self.hero.stats.attack,
            defense=self.enemy.stats.defense,
            feasibility=action_effect.feasibility,
            potential_damage=action_effect.potential_damage,
            n_new_words_in_action=n_new_words_in_action,
            n_overused_words_in_action=n_overused_words_in_action,
            answer_speed_s=timer.interval,
        )

        self.enemy.stats.hp -= damage_calculation_result.total_dmg

        self.creativity_tracker.add_action(proposed_action)

        print(f"Hero turn took: {timer.interval:.2f} seconds")
        print("\n=== HERO TURN ===")
        print(f"🦸 tries to: {proposed_action}")
        print(f"⚡ Effect: {action_effect.effect_description}")
        print(f"  - feasibility: {action_effect.feasibility}")
        print(f"  - potential_damage: {action_effect.potential_damage}")
        print(damage_calculation_result.to_string())
        print(f"❤️  Enemy HP: {self.enemy.stats.hp:.1f}/{self.enemy.stats.max_hp:.1f}\n")

    def enemy_turn(self):
        proposed_enemy_action = self.enemy.get_next_action(self.battle_log, self.hero)

        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_enemy_action,
            attacking_character=self.enemy,
            defending_character=self.hero,
            battle_log_string=self.battle_log.to_string(),
        )

        self.battle_log.add_action(
            BattleEvent(
                character_name=self.enemy.name,
                proposed_action=proposed_enemy_action,
                effect_description=action_effect.effect_description,
            )
        )

        damage_calculation_result = self.damage_calculator.calculate_damage(
            attack=self.enemy.stats.attack,
            defense=self.hero.stats.defense,
            feasibility=action_effect.feasibility,
            potential_damage=action_effect.potential_damage,
            n_new_words_in_action=0,
            n_overused_words_in_action=0,
            answer_speed_s=1000,
        )
        self.hero.stats.hp -= damage_calculation_result.total_dmg

        self.creativity_tracker.add_action(proposed_enemy_action)

        print("\n=== ENEMY TURN ===")
        print(f"👾 tries to: {proposed_enemy_action}")
        print(f"⚡ Effect: {action_effect.effect_description}")
        print(f"  - feasibility: {action_effect.feasibility}")
        print(f"  - potential_damage: {action_effect.potential_damage}")
        print(damage_calculation_result.to_string())
        print(f"❤️  Hero HP: {self.hero.stats.hp:.1f}/{self.hero.stats.max_hp:.1f}\n")

    def start(self):
        print(f"The Battle has started!")
        print(f"🦸 {self.hero.name} lvl {self.hero.stats.level}")
        print(self.hero.description)
        print(
            """
      ,   A           {} 
     / \, | ,        .--.
    |    =|= >      /.--.\ 
     \ /` | `       |====|
      `   |         |`::`|
          |     .-;`\..../`;-.  
         /|\    /  |...::...|  \ 
        / | \  |   /'''::'''\   | 
       /  |  \  \   \   ::   /   /  
      /   |   \ `-._\  ::  /_.-`  
     /    |    \   `-;_::_;-` 
"""
        )

        print("---- VS ----")
        print(f"👾 {self.enemy.name} lvl {self.enemy.stats.level}")
        print(self.enemy.description)
        print(
            """
                      ___====-_  _-====___
                _--^^^#####//      \\#####^^^--_
             _-^##########// (    ) \\##########^-_
            -############//  |\^^/|  \\############-
          _/############//   (@::@)   \\############\_
         /#############((     \\//     ))#############
        -###############\\    (oo)    //###############-
       -#################\\  / "" \  //#################-
      -###################\\/  .  \//###################-
     _#/|##########/\######(   )######/\##########|\#_
    |/ |#/\#/\#/\/  \#/\#|/\#|/\#  /\#/\#/\#/\| \|/|/
    / / _/ /_/ |   |_/_/__/___/_/ | /_/ /_/ // //\ 
    \/\/\/_/ |_/  _/ /_/ \__/  | /_/ /_/ /_/ /_/
            /_/ |_/ /_/  /_/ | /_/ /_/ /_/ /_/ /
           (_/   /_/ |_/(_/  /_/ /_/  /_/ /_/
           (_/   (_/ (_/   (_/  (_/ (_/

"""
        )
        self.advance_turn()

    def advance_turn(self):
        while True:
            self.hero_turn()
            if self.enemy.stats.hp <= 0:
                print(f"{self.enemy.name} is dead!")
                break

            self.enemy_turn()
            if self.hero.stats.hp <= 0:
                print(f"{self.hero.name} is dead!")
                break

            self.hero.end_turn_effects()
