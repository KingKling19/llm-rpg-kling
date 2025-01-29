from llm_rpg.objects.character import Character, Stats
from llm_rpg.objects.item import Item
from llm_rpg.utils.timer import Timer


class ProposedHeroAction:
    def __init__(
        self,
        action: str,
        time_to_answer_seconds: float,
        is_valid: bool,
        invalid_reason: str = None,
    ):
        self.action = action
        self.time_to_answer_seconds = time_to_answer_seconds
        self.is_valid = is_valid
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
        level: int,
        stats: Stats,
        items: list[Item],
        char_per_focus: int = 5,
        battles_won: int = 0,
    ):
        super().__init__(name=name, description=description, level=level, stats=stats)
        self.items = items
        self.char_per_focus = char_per_focus
        self.battles_won = battles_won
        self.should_level_up = False
        self.discovered_item = False

    def win_battle(self):
        self.battles_won += 1
        if self.battles_won % 3 == 0:
            self.should_level_up = True
        if self.battles_won % 2 == 0:
            self.discovered_item = True

    def get_next_action(self) -> ProposedHeroAction:
        with Timer() as timer:
            proposed_input = input()
        n_chars = len(proposed_input.replace(" ", ""))
        if len(proposed_input) == 0:
            return ProposedHeroAction(
                action="Decided to do nothing this turn.",
                is_valid=True,
                # I don't want to give the user an answers speed bonus for doing nothing
                time_to_answer_seconds=100,
            )
        if n_chars > self.char_per_focus * self.stats.focus:
            return ProposedHeroAction(
                action="",
                is_valid=False,
                time_to_answer_seconds=timer.interval,
                invalid_reason=f"Your current focus is {self.stats.focus} which only allows you to type "
                f"{self.char_per_focus * self.stats.focus} characters. You typed {n_chars} non-whitespace characters. Try again.",
            )
        else:
            return ProposedHeroAction(
                action=proposed_input,
                is_valid=True,
                time_to_answer_seconds=timer.interval,
            )

    def render(self):
        print(f"🦸 {self.name} lvl {self.level}")
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
