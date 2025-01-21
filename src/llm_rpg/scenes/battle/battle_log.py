from pydantic import BaseModel

from llm_rpg.scenes.battle.damage_calculator import DamageCalculationResult


class BattleEvent(BaseModel):
    character_name: str
    proposed_action: str
    effect_description: str
    damage_calculation_result: DamageCalculationResult

    class Config:
        arbitrary_types_allowed = True


class BattleLog:
    def __init__(self):
        self.events = []

    def add_event(self, event: BattleEvent):
        self.events.append(event)

    def to_string_for_battle_ai(self, n_actions: int = 5):
        battle_log_text = ""
        for event in self.events[-n_actions:]:
            battle_log_text += (
                f"{event.character_name} turn: {event.effect_description}\n"
            )
        return battle_log_text

    def get_string_of_last_2_events(self):
        if len(self.events) < 2:
            return ""
        text_to_renderer = ""
        last_2_events = self.events[-2:]
        for event in last_2_events:
            text_to_renderer += (
                f"{event.character_name} turn: {event.effect_description}\n"
            )
            text_to_renderer += event.damage_calculation_result.to_string()
            text_to_renderer += "\n\n"
        return text_to_renderer
