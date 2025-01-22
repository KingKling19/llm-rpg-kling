from __future__ import annotations
from enum import Enum

from typing import TYPE_CHECKING

from llm_rpg.objects.character import Enemy, Hero, ProposedHeroAction
from llm_rpg.scenes.battle.battle_ai import BattleAI
from llm_rpg.scenes.battle.battle_log import BattleEvent, BattleLog
from llm_rpg.scenes.battle.creativity_tracker import CreativityTracker
from llm_rpg.scenes.battle.damage_calculator import (
    DamageCalculator,
)
from llm_rpg.scenes.scene import Scene

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


class BattleState(Enum):
    START = "start"
    HERO_COMMAND_INPUT = "hero_command_input"
    HERO_COMMAND_INPUT_INVALID = "hero_command_input_invalid"
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
        self.hero_proposed_action_queue: list[ProposedHeroAction] = []
        self.message_queue: list[str] = []
        self.hero = hero
        self.enemy = enemy
        self.battle_ai = battle_ai
        self.battle_log = BattleLog()
        self.creativity_tracker = CreativityTracker()
        self.damage_calculator = DamageCalculator()

    def handle_input(self):
        if self.current_state == BattleState.START:
            _ = input()
        elif (
            self.current_state == BattleState.HERO_COMMAND_INPUT
            or self.current_state == BattleState.HERO_COMMAND_INPUT_INVALID
        ):
            action = self.hero.get_next_action()
            self.hero_proposed_action_queue.append(action)

    def _update_start_game(self):
        self.current_state = BattleState.HERO_COMMAND_INPUT

    def _update_hero_turn(self):
        proposed_action = self.hero_proposed_action_queue.pop(0)
        if proposed_action.is_valid:
            if proposed_action.is_rest:
                # TODO check if I should send this to the battle_ai
                self.hero.is_resting = True
            self.hero.stats.focus -= proposed_action.focus_cost
            action_effect = self.battle_ai.determine_action_effect(
                proposed_action_attacker=proposed_action.action,
                attacking_character=self.hero,
                defending_character=self.enemy,
                battle_log_string=self.battle_log.to_string_for_battle_ai(),
            )

            n_new_words_in_action = self.creativity_tracker.count_new_words_in_action(
                action=proposed_action.action
            )
            n_overused_words_in_action = (
                self.creativity_tracker.count_overused_words_in_action(
                    action=proposed_action.action
                )
            )
            damage_calculation_result = self.damage_calculator.calculate_damage(
                attack=self.hero.stats.attack,
                defense=self.enemy.stats.defense,
                feasibility=action_effect.feasibility,
                potential_damage=action_effect.potential_damage,
                n_new_words_in_action=n_new_words_in_action,
                n_overused_words_in_action=n_overused_words_in_action,
                answer_speed_s=proposed_action.time_to_answer_seconds,
            )
            self.enemy.stats.hp -= damage_calculation_result.total_dmg
            if self.enemy.stats.hp <= 0:
                self.enemy.stats.hp = 0
            self.creativity_tracker.add_action(proposed_action.action)
            self.battle_log.add_event(
                BattleEvent(
                    is_hero_turn=True,
                    character_name=self.hero.name,
                    proposed_action=proposed_action.action,
                    effect_description=action_effect.effect_description,
                    damage_calculation_result=damage_calculation_result,
                )
            )
            if self.enemy.stats.hp <= 0:
                self.current_state = BattleState.END

        else:
            self.message_queue.append(proposed_action.invalid_reason)
            self.current_state = BattleState.HERO_COMMAND_INPUT_INVALID

    def _update_enemy_turn(self):
        proposed_enemy_action = self.enemy.get_next_action(self.battle_log, self.hero)
        action_effect = self.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_enemy_action,
            attacking_character=self.enemy,
            defending_character=self.hero,
            battle_log_string=self.battle_log.to_string_for_battle_ai(),
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
        if self.hero.stats.hp < 0:
            self.hero.stats.hp = 0
        self.creativity_tracker.add_action(proposed_enemy_action)
        self.battle_log.add_event(
            BattleEvent(
                is_hero_turn=False,
                character_name=self.enemy.name,
                proposed_action=proposed_enemy_action,
                effect_description=action_effect.effect_description,
                damage_calculation_result=damage_calculation_result,
            )
        )
        if self.hero.stats.hp <= 0:
            self.current_state = BattleState.END
        else:
            self.current_state = BattleState.HERO_COMMAND_INPUT

    def _update_end_of_turn_effects(self):
        end_of_turn_effects = self.hero.end_turn_effects()
        self.message_queue.append(end_of_turn_effects.description)

    def update(self):
        if self.current_state == BattleState.START:
            self._update_start_game()
        elif (
            self.current_state == BattleState.HERO_COMMAND_INPUT
            or self.current_state == BattleState.HERO_COMMAND_INPUT_INVALID
        ):
            self._update_hero_turn()
            if self.current_state == BattleState.HERO_COMMAND_INPUT:
                self._update_enemy_turn()
                if self.current_state != BattleState.END:
                    self._update_end_of_turn_effects()
        # battle
        if self.current_state == BattleState.END:
            self.game.is_running = False

    def _clear_screen(self):
        print("\033[2J\033[H", end="")

    def _render_battle_start_state(self):
        self.hero.render()
        self.enemy.render()
        print("Press Enter to start the battle")

    def _render_message_queue(self):
        for message in self.message_queue:
            print(message)
        self.message_queue = []

    def _render_character_stats(self):
        print(
            f"{self.hero.name} HP: {self.hero.stats.hp}/{self.hero.stats.max_hp} Focus: {self.hero.stats.focus}/{self.hero.stats.max_focus}"
        )
        print(f"{self.enemy.name} HP: {self.enemy.stats.hp}/{self.enemy.stats.max_hp}")

    def render(self):
        if self.current_state == BattleState.START:
            self._render_battle_start_state()
        elif self.current_state == BattleState.HERO_COMMAND_INPUT_INVALID:
            print("")
            print("Action invalid because:")
            self._render_message_queue()
            print("")
            print("What do you want to do? You can also type 'rest' to rest this turn.")
        elif (
            self.current_state == BattleState.HERO_COMMAND_INPUT
            or self.current_state == BattleState.END
        ):
            if self.battle_log.events:
                print("")
                print("--- The following events took place... --- \n")
                string_of_last_2_events = self.battle_log.get_string_of_last_2_events()
                print(string_of_last_2_events)
                if self.message_queue:
                    print("--- End of turn status updates --- \n")
                    self._render_message_queue()
                    print("")
            print("--- Current Stats --- \n")
            self._render_character_stats()
            print("")
            if self.current_state == BattleState.END:
                print("Game Ended")
                if self.hero.stats.hp > 0:
                    print(f"{self.hero.name} won!")
                else:
                    print(f"{self.enemy.name} won!")
            else:
                print(
                    "What do you want to do? You can also type 'rest' to rest this turn."
                )
