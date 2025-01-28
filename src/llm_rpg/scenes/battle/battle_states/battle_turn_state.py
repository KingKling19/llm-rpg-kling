from __future__ import annotations

from llm_rpg.objects.hero import ProposedHeroAction
from llm_rpg.systems.battle.battle_log import BattleEvent
from llm_rpg.scenes.battle.battle_states.battle_end_state import BattleEndState

from typing import TYPE_CHECKING

from llm_rpg.scenes.state import State

if TYPE_CHECKING:
    from llm_rpg.scenes.battle.battle_scene import BattleScene


class BattleTurnState(State):
    def __init__(self, battle_scene: BattleScene):
        self.battle_scene = battle_scene
        self.is_hero_input_valid = True
        self.hero_proposed_action_queue: list[ProposedHeroAction] = []
        self.message_queue: list[str] = []

    def handle_input(self):
        action = self.battle_scene.hero.get_next_action()
        self.hero_proposed_action_queue.append(action)

    def _update_hero_turn(self):
        proposed_action = self.hero_proposed_action_queue.pop(0)
        if proposed_action.is_valid:
            self.is_hero_input_valid = True
            if proposed_action.is_rest:
                # TODO check if I should send this to the battle_ai
                self.battle_scene.hero.is_resting = True
            self.battle_scene.hero.stats.focus -= proposed_action.focus_cost
            action_effect = self.battle_scene.battle_ai.determine_action_effect(
                proposed_action_attacker=proposed_action.action,
                attacking_character=self.battle_scene.hero,
                defending_character=self.battle_scene.enemy,
                battle_log_string=self.battle_scene.battle_log.to_string_for_battle_ai(),
            )

            n_new_words_in_action = (
                self.battle_scene.creativity_tracker.count_new_words_in_action(
                    action=proposed_action.action
                )
            )
            n_overused_words_in_action = (
                self.battle_scene.creativity_tracker.count_overused_words_in_action(
                    action=proposed_action.action
                )
            )
            damage_calculation_result = (
                self.battle_scene.damage_calculator.calculate_damage(
                    attack=self.battle_scene.hero.stats.attack,
                    defense=self.battle_scene.enemy.stats.defense,
                    feasibility=action_effect.feasibility,
                    potential_damage=action_effect.potential_damage,
                    n_new_words_in_action=n_new_words_in_action,
                    n_overused_words_in_action=n_overused_words_in_action,
                    answer_speed_s=proposed_action.time_to_answer_seconds,
                )
            )
            self.battle_scene.enemy.stats.hp -= damage_calculation_result.total_dmg
            if self.battle_scene.enemy.stats.hp <= 0:
                self.battle_scene.enemy.stats.hp = 0
            self.battle_scene.creativity_tracker.add_action(proposed_action.action)
            self.battle_scene.battle_log.add_event(
                BattleEvent(
                    is_hero_turn=True,
                    character_name=self.battle_scene.hero.name,
                    proposed_action=proposed_action.action,
                    effect_description=action_effect.effect_description,
                    damage_calculation_result=damage_calculation_result,
                )
            )
        else:
            self.message_queue.append(proposed_action.invalid_reason)
            self.is_hero_input_valid = False

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
                attack=self.battle_scene.enemy.stats.attack,
                defense=self.battle_scene.hero.stats.defense,
                feasibility=action_effect.feasibility,
                potential_damage=action_effect.potential_damage,
                n_new_words_in_action=0,
                n_overused_words_in_action=0,
                answer_speed_s=1000,
            )
        )
        self.battle_scene.hero.stats.hp -= damage_calculation_result.total_dmg
        if self.battle_scene.hero.stats.hp < 0:
            self.battle_scene.hero.stats.hp = 0
        self.battle_scene.creativity_tracker.add_action(proposed_enemy_action)
        self.battle_scene.battle_log.add_event(
            BattleEvent(
                is_hero_turn=False,
                character_name=self.battle_scene.enemy.name,
                proposed_action=proposed_enemy_action,
                effect_description=action_effect.effect_description,
                damage_calculation_result=damage_calculation_result,
            )
        )
        if self.battle_scene.hero.stats.hp <= 0:
            self.battle_scene.change_state(BattleEndState(self.battle_scene))

    def _update_end_of_turn_effects(self):
        end_of_turn_effects = self.battle_scene.hero.end_turn_effects()
        self.message_queue.append(end_of_turn_effects.description)

    def update(self):
        self._update_hero_turn()
        if self.battle_scene.enemy.stats.hp <= 0:
            self.battle_scene.change_state(BattleEndState(self.battle_scene))
            return
        self._update_enemy_turn()
        if self.battle_scene.hero.stats.hp <= 0:
            self.battle_scene.change_state(BattleEndState(self.battle_scene))
            return
        self._update_end_of_turn_effects()

    def _render_message_queue(self):
        for message in self.message_queue:
            print(message)
        self.message_queue = []

    def _render_character_stats(self):
        print(
            f"{self.battle_scene.hero.name} HP: {self.battle_scene.hero.stats.hp}/{self.battle_scene.hero.stats.max_hp} Focus: {self.battle_scene.hero.stats.focus}/{self.battle_scene.hero.stats.max_focus}"
        )
        print(
            f"{self.battle_scene.enemy.name} HP: {self.battle_scene.enemy.stats.hp}/{self.battle_scene.enemy.stats.max_hp}"
        )

    def render(self):
        if not self.is_hero_input_valid:
            print("")
            print("Action invalid because:")
            self._render_message_queue()
            print("")
            print("What do you want to do? You can also type 'rest' to rest this turn.")
        else:
            if self.battle_scene.battle_log.events:
                print("")
                print("--- The following events took place... --- \n")
                string_of_last_2_events = (
                    self.battle_scene.battle_log.get_string_of_last_2_events()
                )
                print(string_of_last_2_events)
            if self.message_queue:
                print("--- End of turn status updates --- \n")
                self._render_message_queue()
                print("")
            print("--- Current Stats --- \n")
            self._render_character_stats()
            print("")
            print("What do you want to do? You can also type 'rest' to rest this turn.")
