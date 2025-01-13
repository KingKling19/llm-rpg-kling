from math import ceil, floor
import random


class DamageCalculationResult:
    def __init__(
        self,
        random_factor: float,
        base_dmg: float,
        feasibility: float,
        potential_damage: float,
        llm_dmg_impact: float,
        llm_dmg_scaling: float,
        new_words_bonus: float,
        overused_words_penalty: float,
        creativity_bonus_scaling: float,
        answer_speed_s: float,
        answer_speed_bonus_scaling: float,
        llm_scaled_base_dmg: float,
        creativity_bonus_dmg: float,
        answer_speed_bonus_dmg: float,
        total_dmg_unrounded: float,
        total_dmg: float,
    ):
        self.random_factor = random_factor
        self.base_dmg = base_dmg
        self.feasibility = feasibility
        self.potential_damage = potential_damage
        self.llm_dmg_impact = llm_dmg_impact
        self.llm_dmg_scaling = llm_dmg_scaling
        self.new_words_bonus = new_words_bonus
        self.overused_words_penalty = overused_words_penalty
        self.creativity_bonus_scaling = creativity_bonus_scaling
        self.answer_speed_s = answer_speed_s
        self.answer_speed_bonus_scaling = answer_speed_bonus_scaling
        self.llm_scaled_base_dmg = llm_scaled_base_dmg
        self.creativity_bonus_dmg = creativity_bonus_dmg
        self.answer_speed_bonus_dmg = answer_speed_bonus_dmg
        self.total_dmg_unrounded = total_dmg_unrounded
        self.total_dmg = total_dmg

    def to_string_debug(self):
        return (
            f"💥 Damage dealt: {self.total_dmg}\n"
            f"  - random_factor: {self.random_factor}\n"
            f"  - base_dmg: {self.base_dmg}\n"
            f"  - feasibility: {self.feasibility}\n"
            f"  - potential_damage: {self.potential_damage}\n"
            f"  - llm_dmg_impact: {self.llm_dmg_impact}\n"
            f"  - llm_dmg_scaling: {self.llm_dmg_scaling}\n"
            f"  - llm_scaled_base_dmg: {self.llm_scaled_base_dmg}\n"
            f"  - new_words_bonus: {self.new_words_bonus}\n"
            f"  - overused_words_penalty: {self.overused_words_penalty}\n"
            f"  - creativity_bonus_scaling: {self.creativity_bonus_scaling}\n"
            f"  - creativity_bonus_dmg: {self.creativity_bonus_dmg}\n"
            f"  - answer_speed_s: {self.answer_speed_s}\n"
            f"  - answer_speed_bonus_scaling: {self.answer_speed_bonus_scaling}\n"
            f"  - answer_speed_bonus_dmg: {self.answer_speed_bonus_dmg}\n"
            f"  - total_dmg_unrounded: {self.total_dmg_unrounded}\n"
        )


class DamageCalculator:
    def __init__(
        self,
        # base dmg scaling
        attack_scaling: float = 0.5,
        defense_scaling: float = 0.25,
        random_factor_max: float = 1.05,
        random_factor_min: float = 0.95,
        # how much llm can affect base dmg
        llm_dmg_impact: int = 2,
        # bonus scaling increments / reductions
        answer_speed_bonus_reduction_per_s: float = 0.04,
        new_words_bonus_increment_per_word: float = 0.05,
        overused_words_penalty_increment_per_word: float = 0.02,
        # max bonus scaling
        max_answer_speed_bonus: float = 0.2,
        max_new_words_bonus: float = 1,
        max_overused_words_penalty: float = 0.2,
    ):
        self.attack_scaling = attack_scaling
        self.defense_scaling = defense_scaling
        self.random_factor_max = random_factor_max
        self.random_factor_min = random_factor_min
        self.llm_dmg_impact = llm_dmg_impact
        self.answer_speed_bonus_reduction_per_s = answer_speed_bonus_reduction_per_s
        self.new_words_bonus_increment_per_word = new_words_bonus_increment_per_word
        self.overused_words_penalty_increment_per_word = (
            overused_words_penalty_increment_per_word
        )
        self.max_answer_speed_bonus = max_answer_speed_bonus
        self.max_new_words_bonus = max_new_words_bonus
        self.max_overused_words_penalty = max_overused_words_penalty

    def calculate_damage(
        self,
        attack: float,
        defense: float,
        feasibility: float,
        potential_damage: float,
        n_new_words_in_action: int,
        n_overused_words_in_action: int,
        answer_speed_s: float,
    ) -> DamageCalculationResult:
        # base dmg depends purely on stats and random factor
        random_factor = random.uniform(self.random_factor_min, self.random_factor_max)
        base_dmg = max(
            1,
            (attack * self.attack_scaling - defense * self.defense_scaling)
            * random_factor,
        )

        # llm dmg depends on feasibility and potential damage
        llm_dmg_scaling = self.llm_dmg_impact * feasibility * potential_damage
        llm_scaled_base_dmg = base_dmg * llm_dmg_scaling

        # creativity bonus depends on new words bonus and overused words penalty
        new_words_bonus = (
            self.new_words_bonus_increment_per_word * n_new_words_in_action
        )
        overused_words_penalty = (
            self.overused_words_penalty_increment_per_word * n_overused_words_in_action
        )

        creativity_bonus_scaling = new_words_bonus - overused_words_penalty
        if creativity_bonus_scaling < 0:
            # penalty gets floored
            creativity_bonus_dmg = floor(llm_scaled_base_dmg * creativity_bonus_scaling)
        else:
            # bonus gets ceiled
            creativity_bonus_dmg = ceil(llm_scaled_base_dmg * creativity_bonus_scaling)

        # answer speed bonus depends on answer speed
        answer_speed_bonus_scaling = max(
            0,
            self.max_answer_speed_bonus
            - (self.answer_speed_bonus_reduction_per_s * answer_speed_s),
        )
        answer_speed_bonus_dmg = ceil(llm_scaled_base_dmg * answer_speed_bonus_scaling)

        # total dmg is sum of llm_scaled_base_dmg and all bonuses
        total_dmg_unrounded = (
            llm_scaled_base_dmg + creativity_bonus_dmg + answer_speed_bonus_dmg
        )
        total_dmg = round(total_dmg_unrounded)
        if total_dmg < 1:
            total_dmg = 1

        return DamageCalculationResult(
            random_factor=random_factor,
            base_dmg=base_dmg,
            feasibility=feasibility,
            potential_damage=potential_damage,
            llm_dmg_impact=self.llm_dmg_impact,
            llm_dmg_scaling=llm_dmg_scaling,
            new_words_bonus=new_words_bonus,
            overused_words_penalty=overused_words_penalty,
            creativity_bonus_scaling=creativity_bonus_scaling,
            answer_speed_s=answer_speed_s,
            answer_speed_bonus_scaling=answer_speed_bonus_scaling,
            llm_scaled_base_dmg=llm_scaled_base_dmg,
            creativity_bonus_dmg=creativity_bonus_dmg,
            answer_speed_bonus_dmg=answer_speed_bonus_dmg,
            total_dmg_unrounded=total_dmg_unrounded,
            total_dmg=total_dmg,
        )
