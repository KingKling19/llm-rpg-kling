from llm_rpg.objects.character import Character, Stats
from llm_rpg.objects.item import Item
from llm_rpg.utils.timer import Timer


class ProposedHeroAction:
    def __init__(
        self,
        action: str,
        focus_cost: int,
        time_to_answer_seconds: float,
        is_valid: bool,
        is_rest: bool,
        invalid_reason: str = None,
    ):
        self.action = action
        self.focus_cost = focus_cost
        self.time_to_answer_seconds = time_to_answer_seconds
        self.is_valid = is_valid
        self.is_rest = is_rest
        self.invalid_reason = invalid_reason


class EndOfTurnEffects:
    def __init__(self, focus_restored: int, hp_restored: int, description: str):
        self.focus_restored = focus_restored
        self.hp_restored = hp_restored
        self.description = description


class Hero(Character):
    def __init__(
        self,
        name: str,
        description: str,
        stats: Stats,
        gold: int,
        items: list[Item],
        battles_won: int = 0,
        char_per_focus: int = 5,
        focus_restoration_per_turn: int = 1,
        focus_restoration_per_rest: int = 2,
    ):
        super().__init__(name, description, stats)
        self.gold = gold
        self.items = items
        self.char_per_focus = char_per_focus
        self.focus_restoration_per_turn = focus_restoration_per_turn
        self.focus_restoration_per_rest = focus_restoration_per_rest
        self.is_resting = False
        self.battles_won = battles_won
        self.should_level_up = False

    def win_battle(self):
        self.battles_won += 1
        if self.battles_won % 3 == 0:
            self.should_level_up = True

    def get_next_action(self) -> ProposedHeroAction:
        with Timer() as timer:
            proposed_input = input()
        if proposed_input.lower().strip() == "rest":
            return ProposedHeroAction(
                action="Is tired and rests this turn.",
                focus_cost=0,
                is_valid=True,
                is_rest=True,
                time_to_answer_seconds=timer.interval,
            )

        n_chars = len(proposed_input.replace(" ", ""))
        if n_chars > self.char_per_focus * self.stats.focus:
            return ProposedHeroAction(
                action="",
                focus_cost=0,
                is_valid=False,
                is_rest=False,
                time_to_answer_seconds=timer.interval,
                invalid_reason=f"Your current focus is {self.stats.focus} which only allows you to type "
                f"{self.char_per_focus * self.stats.focus} characters. You typed {n_chars} non-whitespace characters. Try again.",
            )

        used_focus = max(1, n_chars // self.char_per_focus)
        return ProposedHeroAction(
            action=proposed_input,
            focus_cost=used_focus,
            is_valid=True,
            is_rest=False,
            time_to_answer_seconds=timer.interval,
        )

    def end_turn_effects(self) -> EndOfTurnEffects:
        if self.is_resting:
            focus_to_restore = self.focus_restoration_per_rest
        else:
            focus_to_restore = self.focus_restoration_per_turn

        self.is_resting = False

        if self.stats.focus < self.stats.max_focus:
            focus_to_restore = min(
                focus_to_restore, self.stats.max_focus - self.stats.focus
            )
            if focus_to_restore > 0:
                self.stats.focus += focus_to_restore
                if self.is_resting:
                    return EndOfTurnEffects(
                        focus_restored=focus_to_restore,
                        hp_restored=0,
                        description=f"You have rested and restored {focus_to_restore} focus points. "
                        f"You now have {self.stats.focus} focus points.",
                    )
                else:
                    return EndOfTurnEffects(
                        focus_restored=focus_to_restore,
                        hp_restored=0,
                        description=f"You restore {focus_to_restore} focus points. "
                        f"You now have {self.stats.focus} focus points.",
                    )
        else:
            return EndOfTurnEffects(
                focus_restored=0,
                hp_restored=0,
                description="You restore no focus points. As you have reached your maximum focus of "
                f"{self.stats.max_focus}.",
            )

    def render(self):
        print(f"🦸 {self.name} lvl {self.stats.level}")
        print(self.description)
        print(
            """
      ,   A           {} 
     / \, | ,        .--.
    |    =|= >      /.--.\ 
     \ /` | `       |====|
      `   |         |`::`|
          |     .-;`\..../`;-.  
         /|\    /  |...::...|  \ 
        / | \  |   /'''::'''\   | 
       /  |  \  \   \   ::   /   /  
      /   |   \ `-._\  ::  /_.-`  
     /    |    \   `-;_::_;-` 
"""
        )
