from textwrap import dedent
from llm_rpg.llm.llm import LLM
from llm_rpg.scenes.battle.battle_log import BattleLog
from llm_rpg.utils.timer import Timer


class Stats:
    def __init__(self, level: int, attack: int, defense: int, focus: int, hp: int):
        self.level = level
        # scales damage inflicted
        self.attack = attack
        # reduces damage taken
        self.defense = defense
        # determines amount of letters you can type
        self.max_focus = focus
        self.focus = focus
        # determines how much damage you can take
        self.max_hp = hp
        self.hp = hp


class Character:
    def __init__(self, name: str, description: str, stats: Stats):
        # name of the character
        self.name = name
        # description of th character, also includes the items they have equipped
        self.description = description
        # stats of the character
        self.stats = stats


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
        char_per_focus: int = 5,
        focus_restoration_per_turn: int = 1,
        focus_restoration_per_rest: int = 2,
    ):
        super().__init__(name, description, stats)
        self.char_per_focus = char_per_focus
        self.focus_restoration_per_turn = focus_restoration_per_turn
        self.focus_restoration_per_rest = focus_restoration_per_rest
        self.is_resting = False

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


class Enemy(Character):
    def __init__(self, name: str, description: str, stats: Stats, llm: LLM):
        super().__init__(name, description, stats)
        self.llm = llm

    def get_next_action(self, battle_log: BattleLog, hero: Hero):
        battle_log_text = battle_log.to_string_for_battle_ai()

        prompt = dedent(
            f"""
            You are a video game character called {self.name} that is in a battle against an enemy called {hero.name}.
            Try to come up with a natural action based on the battle history and the current HP of both characters.
            
            You should try to defeat the enemy or reduce their HP to 0.

            Don't repeat the same action every turn.
            
            You have the following description:
            {self.description}

            The enemy, {hero.name}, has the following description:
            {hero.description}

            Current battle history:
            {battle_log_text}

            HP of you, {self.name}: {self.stats.hp}
            HP of {hero.name}: {hero.stats.hp}
            
            Describe your next action very briefly in third person like a narrator would.
            """
        )

        return self.llm.generate_completion(prompt)

    def render(self):
        print(f"👾 {self.name} lvl {self.stats.level}")
        print(self.description)
        print(
            """
                      ___====-_  _-====___
                _--^^^#####//      \\#####^^^--_
             _-^##########// (    ) \\##########^-_
            -############//  |\^^/|  \\############-
          _/############//   (@::@)   \\############\_
         /#############((     \\//     ))#############
        -###############\\    (oo)    //###############-
       -#################\\  / "" \  //#################-
      -###################\\/  .  \//###################-
     _#/|##########/\######(   )######/\##########|\#_
    |/ |#/\#/\#/\/  \#/\#|/\#|/\#  /\#/\#/\#/\| \|/|/
    / / _/ /_/ |   |_/_/__/___/_/ | /_/ /_/ // //\ 
    \/\/\/_/ |_/  _/ /_/ \__/  | /_/ /_/ /_/ /_/
            /_/ |_/ /_/  /_/ | /_/ /_/ /_/ /_/ /
           (_/   /_/ |_/(_/  /_/ /_/  /_/ /_/
           (_/   (_/ (_/   (_/  (_/ (_/

"""
        )
