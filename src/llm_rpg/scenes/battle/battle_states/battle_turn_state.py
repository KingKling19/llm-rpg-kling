from __future__ import annotations

from llm_rpg.scenes.battle.battle_states.battle_states import BattleStates
from llm_rpg.systems.battle.damage_calculator import DamageCalculationResult
from llm_rpg.systems.hero.hero import ProposedHeroAction
from llm_rpg.systems.battle.battle_log import BattleEvent
from llm_rpg.scenes.battle.battle_states.battle_end_state import BattleEndState

from typing import TYPE_CHECKING

from llm_rpg.scenes.state import State
from llm_rpg.utils.rendering import render_state_transition_header

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleTurnState(State):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene
        self.is_hero_input_valid = True
        self.proposed_hero_action: ProposedHeroAction = None
        self.display_state_transition_header = True

    def handle_input(self):
        self.proposed_hero_action = self.battle_scene.hero.get_next_action()

    def _update_hero_turn(self):
        action_effect = self.battle_scene.battle_ai.determine_action_effect(
            proposed_action_attacker=self.proposed_hero_action.action,
            attacking_character=self.battle_scene.hero,
            defending_character=self.battle_scene.enemy,
            battle_log_string=self.battle_scene.battle_log.to_string_for_battle_ai(),
        )

        n_new_words_in_action = (
            self.battle_scene.creativity_tracker.count_new_words_in_action(
                action=self.proposed_hero_action.action
            )
        )
        n_overused_words_in_action = (
            self.battle_scene.creativity_tracker.count_overused_words_in_action(
                action=self.proposed_hero_action.action
            )
        )
        damage_calculation_result: DamageCalculationResult = (
            self.battle_scene.damage_calculator.calculate_damage(
                attack=self.battle_scene.hero.get_current_stats().attack,
                defense=self.battle_scene.enemy.get_current_stats().defense,
                feasibility=action_effect.feasibility,
                potential_damage=action_effect.potential_damage,
                n_new_words_in_action=n_new_words_in_action,
                n_overused_words_in_action=n_overused_words_in_action,
                answer_speed_s=self.proposed_hero_action.time_to_answer_seconds,
                equiped_items=self.battle_scene.hero.inventory.items,
            )
        )
        self.battle_scene.enemy.inflict_damage(damage_calculation_result.total_dmg)
        self.battle_scene.creativity_tracker.add_action(
            self.proposed_hero_action.action
        )
        self.battle_scene.battle_log.add_event(
            BattleEvent(
                is_hero_turn=True,
                character_name=self.battle_scene.hero.name,
                proposed_action=self.proposed_hero_action.action,
                effect_description=action_effect.effect_description,
                damage_calculation_result=damage_calculation_result,
            )
        )

    def _update_enemy_turn(self):
        proposed_enemy_action = self.battle_scene.enemy.get_next_action(
            self.battle_scene.battle_log, self.battle_scene.hero
        )
        action_effect = self.battle_scene.battle_ai.determine_action_effect(
            proposed_action_attacker=proposed_enemy_action,
            attacking_character=self.battle_scene.enemy,
            defending_character=self.battle_scene.hero,
            battle_log_string=self.battle_scene.battle_log.to_string_for_battle_ai(),
        )
        damage_calculation_result = (
            self.battle_scene.damage_calculator.calculate_damage(
                attack=self.battle_scene.enemy.get_current_stats().attack,
                defense=self.battle_scene.hero.get_current_stats().defense,
                feasibility=action_effect.feasibility,
                potential_damage=action_effect.potential_damage,
                n_new_words_in_action=0,
                n_overused_words_in_action=0,
                answer_speed_s=1000,
                equiped_items=[],
            )
        )

        self.battle_scene.hero.inflict_damage(damage_calculation_result.total_dmg)

        self.battle_scene.battle_log.add_event(
            BattleEvent(
                is_hero_turn=False,
                character_name=self.battle_scene.enemy.name,
                proposed_action=proposed_enemy_action,
                effect_description=action_effect.effect_description,
                damage_calculation_result=damage_calculation_result,
            )
        )

    def update(self):
        self.display_state_transition_header = False
        if self.proposed_hero_action.is_valid:
            self._update_hero_turn()
            if self.battle_scene.enemy.is_dead():
                self.battle_scene.change_state(BattleStates.END)
                return
            self._update_enemy_turn()
            if self.battle_scene.hero.is_dead():
                self.battle_scene.change_state(BattleStates.END)
                return

    def _render_character_stats(self):
        print("- Stats - \n")
        print(
            f"{self.battle_scene.hero.name} HP: {self.battle_scene.hero.hp}/{self.battle_scene.hero.get_current_stats().max_hp}"
        )
        print(
            f"{self.battle_scene.enemy.name} HP: {self.battle_scene.enemy.hp}/{self.battle_scene.enemy.get_current_stats().max_hp}"
        )

    def _render_ask_for_hero_action(self):
        chars_can_type = self.battle_scene.hero.get_current_stats().focus
        print(
            f"What do you want to do? Your focus allows you to type {chars_can_type} characters."
        )

    def _render_invalid_hero_action(self):
        print("")
        print("Action invalid because:")
        print(self.proposed_hero_action.invalid_reason)

    def _render_battle_log(self):
        if self.battle_scene.battle_log.events:
            print("")
            print("--- The following events took place... --- \n")
            string_of_last_2_events = (
                self.battle_scene.battle_log.get_string_of_last_2_events()
            )
            print(string_of_last_2_events)

    def render(self):
        if self.display_state_transition_header:
            render_state_transition_header("Battle has started")
        if self.proposed_hero_action and (not self.proposed_hero_action.is_valid):
            self._render_invalid_hero_action()
        else:
            self._render_battle_log()
            self._render_character_stats()
        print("")
        self._render_ask_for_hero_action()
