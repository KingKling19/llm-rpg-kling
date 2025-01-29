from pydantic import BaseModel

from llm_rpg.systems.battle.damage_calculator import DamageCalculationResult


class BattleEvent(BaseModel):
    is_hero_turn: bool
    character_name: str
    proposed_action: str
    effect_description: str
    damage_calculation_result: DamageCalculationResult

    class Config:
        arbitrary_types_allowed = True


class BattleLog:
    def __init__(self):
        self.events: list[BattleEvent] = []

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
        if len(self.events) == 0:
            return ""
        string_repr = ""
        last_2_events = self.events[-2:]
        for i, event in enumerate(last_2_events):
            if event.is_hero_turn:
                string_repr += "🦸 Your turn:\n"
            else:
                string_repr += "👾 Enemy turn:\n"
            string_repr += (
                f"{event.character_name} tried to {event.proposed_action}\n\n"
                f"LLM estimates:\n"
                f"- feasibility: {event.damage_calculation_result.feasibility}\n"
                f"- potential damage: {event.damage_calculation_result.potential_damage}\n\n"
                f"Effect:\n"
                f"{event.effect_description}\n\n"
                f"Damage inflicted:\n"
                f"{event.damage_calculation_result.to_string()}\n"
            )
            if i < len(last_2_events) - 1:
                string_repr += "\n"
        return string_repr
