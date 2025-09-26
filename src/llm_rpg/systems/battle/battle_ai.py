from pydantic import BaseModel, Field
import json
from llm_rpg.llm.llm import LLM, OpenAILLM

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
                "How feasible the action is, ranging from 0 to 10. A value of 0 indicates the action is "
                "completely infeasible, while a value of 10 indicates it is fully feasible."
            ),
        ),
    ]
    potential_damage: Annotated[
        float,
        Field(
            ge=0,
            le=10,
            description=(
                "Potential damage the action can inflict, ranging from 0 to 10. A score of 0 means the action "
                "causes no damage, whereas a score of 10 means it causes maximum possible damage."
            ),
        ),
    ]
    effect_description: str = Field(
        description=(
            "A single sentence brief description of the effect of the action. It should concretely, deterministically describe what happened. If the action is infeasible give the reason why."
        )
    )


class BattleAI:
    def __init__(self, llm: LLM, effect_determination_prompt: str, debug: bool = False):
        self.llm = llm
        self.effect_determination_prompt = effect_determination_prompt
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
        hero_name = hero.name
        if is_hero_attacker:
            attacker_name = hero.name
            defender_name = enemy.name
            attacker_description = hero.description
            defender_description = enemy.description
        else:
            attacker_name = enemy.name
            defender_name = hero.name
            attacker_description = enemy.description
            defender_description = hero.description
        return self.effect_determination_prompt.format(
            attacker_name=attacker_name,
            defender_name=defender_name,
            attacker_description=attacker_description,
            defender_description=defender_description,
            hero_name=hero_name,
            items_hero=items_hero,
            battle_log_string=battle_log_string,
            proposed_action_attacker=proposed_action_attacker,
        )

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
            prompt += (
                "\nRespond with a JSON object containing the keys "
                "\"feasibility\", \"potential_damage\", and "
                "\"effect_description\". Feasibility and potential_damage "
                "must be numbers between 0 and 10."
            )
            schema = json.dumps(ActionEffect.model_json_schema(), indent=2)
            if not isinstance(self.llm, OpenAILLM):
                # Groq and Ollama benefit from seeing the JSON schema directly; OpenAI structured output does not
                prompt += "\n" + schema

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
