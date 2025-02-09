import json
from textwrap import dedent
from pydantic import BaseModel, Field

from llm_rpg.llm.llm import LLM

from typing import Annotated

from llm_rpg.objects.item import Item
from llm_rpg.systems.battle.enemy import Enemy
from llm_rpg.systems.hero.hero import Hero


class ActionEffect(BaseModel):
    feasibility: Annotated[
        float,
        Field(
            ge=0,
            le=10,
            description=(
                "Represents how feasible the action is, ranging from 0 to 10. A value of 0 indicates the action is "
                "completely infeasible, while a value of 10 indicates it is fully feasible. This should depend on the "
                "history of the battle and the effect_description."
            ),
        ),
    ]
    potential_damage: Annotated[
        float,
        Field(
            ge=0,
            le=10,
            description=(
                "Represents the potential damage the action can inflict, ranging from 0 to 10. A score of 0 means the action "
                "causes no damage, whereas a score of 10 means it causes maximum possible damage. This should depend on the "
                "history of the battle and the effect_description."
            ),
        ),
    ]
    effect_description: str = Field(
        description=(
            "A single sentence brief description of the effect of the action. It should concretely, deterministically describe what happened"
        )
    )


class BattleAI:
    def __init__(self, llm: LLM, debug: bool = False):
        self.llm = llm
        self.debug = debug

    def _format_items(self, items: list[Item]) -> str:
        return "\n".join([f"  - {item.name}: {item.description}" for item in items])

    def _get_battle_ai_prompt(
        self,
        hero: Hero,
        enemy: Enemy,
        is_hero_attacker: bool,
        battle_log_string: str,
        proposed_action_attacker: str,
    ) -> str:
        items_hero = self._format_items(hero.inventory.items)
        if is_hero_attacker:
            prompt = dedent(
                f"""
                You are a video game ai that determines the effect of proposed actions in a battle
                between two characters.

                The characters are:
                - {hero.name}
                - {enemy.name}

                {hero.name} is attacking {enemy.name}.

                {hero.name} description:
                {hero.description}

                {enemy.name} description:
                {enemy.description}

                {hero.name} items in inventory:
                {items_hero}

                Battle history:
                {battle_log_string}

                Proposed action of {hero.name}:
                {proposed_action_attacker}

                You should determine what happens next. Take into account the battle history as
                actions should have different effects depending on the history.

                Also take into account the current HP and description of both characters.

                Especially pay attention to the items of {hero.name} as {hero.name} should only be able to use items that are in his inventory.
                Usage of other items is infeasible.
                
                Important: repeated actions by {hero.name} should have reduced potential damage, look in the battle history for past actions.
                Vaguely worded actions should also have reduced potential damage as I want to promote precise or verbose actions.

                I need you to output the effect of the proposed action in the following JSON format:
            """
            )
            return prompt
        else:
            prompt = dedent(
                f"""
                You are a video game ai that determines the effect of proposed actions in a battle
                between two characters.

                The characters are:
                - {hero.name}
                - {enemy.name}

                {enemy.name} is attacking {hero.name}.

                {hero.name} description:
                {hero.description}

                {enemy.name} description:
                {enemy.description}

                {hero.name} items in inventory:
                {items_hero}

                Battle history:
                {battle_log_string}

                Proposed action of {enemy.name}:
                {proposed_action_attacker}

                You should determine what happens next. Take into account the battle history as
                actions should have different effects depending on the history.

                Also take into account the current HP and description of both characters.

                Also pay attention to the items of {hero.name} as the damage of {enemy.name}
                can be influenced by the items of {hero.name}.

                I need you to output the effect of the proposed action in the following JSON format:
            """
            )
            return prompt

    def determine_action_effect(
        self,
        proposed_action_attacker: str,
        hero: Hero,
        enemy: Enemy,
        is_hero_attacker: bool,
        battle_log_string: str,
    ) -> ActionEffect:
        attempts = 0
        while attempts < 3:
            prompt = self._get_battle_ai_prompt(
                hero=hero,
                enemy=enemy,
                is_hero_attacker=is_hero_attacker,
                battle_log_string=battle_log_string,
                proposed_action_attacker=proposed_action_attacker,
            )
            schema = json.dumps(ActionEffect.model_json_schema(), indent=2)
            prompt += schema

            if self.debug:
                print("////////////DEBUG BattleAI prompt////////////")
                print(prompt)
                print("////////////DEBUG BattleAI prompt////////////")

            try:
                unscaled_output = self.llm.generate_structured_completion(
                    prompt=prompt, output_model=ActionEffect
                )
                unscaled_output.feasibility = unscaled_output.feasibility / 10
                unscaled_output.potential_damage = unscaled_output.potential_damage / 10
                return unscaled_output
            except Exception as e:
                print(e)
                attempts += 1
                continue

        raise ValueError("Failed to determine action effect")
