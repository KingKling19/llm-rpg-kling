import json
from textwrap import dedent
from pydantic import BaseModel, Field

from llm_rpg.llm.llm import LLM

from typing import Annotated
from pydantic import BaseModel, Field

from llm_rpg.objects.character import Character


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
    def __init__(self, llm: LLM):
        self.llm = llm

    def determine_action_effect(
        self,
        proposed_action_attacker: str,
        attacking_character: Character,
        defending_character: Character,
        battle_log_string: str,
    ) -> ActionEffect:
        attempts = 0
        while attempts < 3:
            prompt = dedent(
                f"""
                You are a video game ai that determines the effect of proposed actions in a battle
                between two characters.

                The characters are:
                - {attacking_character.name}
                - {defending_character.name}

                {attacking_character.name} is attacking {defending_character.name}.

                {attacking_character.name} description:
                {attacking_character.description}

                {defending_character.name} description:
                {defending_character.description}

                Battle history:
                {battle_log_string}

                Proposed action of {attacking_character.name}:
                {proposed_action_attacker}

                You should determine what happens next. Take into account the battle history as
                actions should have different effects depending on the history.

                Also take into account the current HP and description of both characters.

                I need you to output the effect of the proposed action in the following JSON format:
            """
            )
            schema = json.dumps(ActionEffect.model_json_schema(), indent=2)
            prompt += schema

            # print("=== PROMPT BATTLE AI ===")
            # print(prompt)

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
