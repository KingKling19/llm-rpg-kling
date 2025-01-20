from __future__ import annotations
from enum import Enum

from typing import TYPE_CHECKING

from llm_rpg.objects.character import Enemy, Hero
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_log import BattleEvent, BattleLog
from llm_rpg.scenes.battle.creativity_tracker import CreativityTracker
from llm_rpg.scenes.battle.damage_calculator import (
    DamageCalculationResult,
    DamageCalculator,
)
from llm_rpg.scenes.scene import Scene
from llm_rpg.utils.timer import Timer

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class BattleState(Enum):
    START = "start"
    HERO_COMMAND_INPUT = "hero_command_input"
    END = "end"


class BattleScene(Scene):
    def __init__(
        self,
        game: Game,
        hero: Hero,
        enemy: Enemy,
        battle_ai: BattleAI,
    ):
        super().__init__(game)
        self.current_state = BattleState.START
        self.input_command_queue = []
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker()
        self.damage_calculator = DamageCalculator()
        self.damage_calculation_results_queue: list[DamageCalculationResult] = []

    def handle_input(self):
        if self.current_state == BattleState.START:
            _ = input()
        elif self.current_state == BattleState.HERO_COMMAND_INPUT:
            with Timer() as timer:
                action = self.hero.get_next_action()
            self.input_command_queue.append({"action": action, "time": timer.interval})

    def _update_start_game(self):
        self.current_state = BattleState.HERO_COMMAND_INPUT

    def _update_hero_turn(self):
        command = self.input_command_queue.pop(0)
        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=command["action"],
            attacking_character=self.hero,
            defending_character=self.enemy,
            battle_log_string=self.battle_log.to_string(),
        )
        self.battle_log.add_action(
            BattleEvent(
                character_name=self.hero.name,
                proposed_action=command["action"],
                effect_description=action_effect.effect_description,
            )
        )
        n_new_words_in_action = self.creativity_tracker.count_new_words_in_action(
            action=command["action"]
        )
        n_overused_words_in_action = (
            self.creativity_tracker.count_overused_words_in_action(
                action=command["action"]
            )
        )
        damage_calculation_result = self.damage_calculator.calculate_damage(
            attack=self.hero.stats.attack,
            defense=self.enemy.stats.defense,
            feasibility=action_effect.feasibility,
            potential_damage=action_effect.potential_damage,
            n_new_words_in_action=n_new_words_in_action,
            n_overused_words_in_action=n_overused_words_in_action,
            answer_speed_s=command["time"],
        )
        self.enemy.stats.hp -= damage_calculation_result.total_dmg
        self.creativity_tracker.add_action(command["action"])
        self.damage_calculation_results_queue.append(damage_calculation_result)
        if self.enemy.stats.hp <= 0:
            self.current_state = BattleState.END

    def _update_enemy_turn(self):
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
        self.damage_calculation_results_queue.append(damage_calculation_result)
        if self.hero.stats.hp <= 0:
            self.current_state = BattleState.END
        else:
            self.current_state = BattleState.HERO_COMMAND_INPUT

    def update(self):
        if self.current_state == BattleState.START:
            self._update_start_game()
        elif self.current_state == BattleState.HERO_COMMAND_INPUT:
            self.damage_calculation_results_queue = []
            self._update_hero_turn()
            self._update_enemy_turn()
        elif self.current_state == BattleState.END:
            self.game.is_running = False

    def _clear_screen(self):
        print("\033[2J\033[H", end="")

    def render(self):
        self._clear_screen()
        if self.current_state == BattleState.START:
            self.hero.render()
            self.enemy.render()
            print("Press Any Key to start the battle")
        elif (
            self.current_state == BattleState.HERO_COMMAND_INPUT
            or self.current_state == BattleState.END
        ):
            for damage_calculation_result in self.damage_calculation_results_queue:
                print(damage_calculation_result.to_string())
            print("-" * 100)
            print(f"{self.hero.name} HP: {self.hero.stats.hp}/{self.hero.stats.max_hp}")
            print(
                f"{self.enemy.name} HP: {self.enemy.stats.hp}/{self.enemy.stats.max_hp}"
            )
            if self.current_state == BattleState.END:
                print("Game Ended")
            else:
                print("What do you want to do?")
