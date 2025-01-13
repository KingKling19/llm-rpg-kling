from textwrap import dedent
from llm_rpg.llm.llm import LLM
from llm_rpg.scenes.battle.battle_log import BattleLog


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
        self.has_rested = False

    def get_next_action(self):
        proposed_input = input(
            f"What is your next action? You have {self.stats.focus} focus "
            f"so you can type {self.char_per_focus * self.stats.focus} non-whitespace characters. "
            f"You can also type 'rest' to rest this turn. \n"
        )
        n_chars = len(proposed_input.replace(" ", ""))
        if proposed_input.lower().strip() == "rest":
            self.has_rested = True
            return "Is tired and rests this turn."
        while n_chars > self.char_per_focus * self.stats.focus:
            print(
                f"Your current focus is {self.stats.focus} which only allows you to type "
                f"{self.char_per_focus * self.stats.focus} characters. You typed {n_chars} non-whitespace characters. Try again."
            )
            proposed_input = input(
                f"What is your next action? You have {self.stats.focus} focus "
                f"so you can type {self.char_per_focus * self.stats.focus} non-whitespace characters. "
                f"You can also type 'rest' to rest this turn. \n "
            )
            n_chars = len(proposed_input.replace(" ", ""))

        used_focus = max(1, n_chars // self.char_per_focus)
        self.stats.focus -= used_focus
        print(
            f"You used {used_focus} focus points. You now have {self.stats.focus} focus points."
        )
        return proposed_input

    def end_turn_effects(self):
        if self.has_rested:
            focus_to_restore = self.focus_restoration_per_rest
        else:
            focus_to_restore = self.focus_restoration_per_turn

        if self.stats.focus < self.stats.max_focus:
            focus_to_restore = min(
                focus_to_restore, self.stats.max_focus - self.stats.focus
            )
            if focus_to_restore > 0:
                self.stats.focus += focus_to_restore
                if self.has_rested:
                    print(
                        f"You have rested and restored {focus_to_restore} focus points. "
                        f"You now have {self.stats.focus} focus points."
                    )
                else:
                    print(
                        f"You restore {focus_to_restore} focus points. "
                        f"You now have {self.stats.focus} focus points."
                    )
        else:
            print(
                f"You restore no focus points. As you have reached your maximum focus of {self.stats.max_focus}."
            )

        self.has_rested = False


class Enemy(Character):
    def __init__(self, name: str, description: str, stats: Stats, llm: LLM):
        super().__init__(name, description, stats)
        self.llm = llm

    def get_next_action(self, battle_log: BattleLog, hero: Hero):
        battle_log_text = battle_log.to_string()

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
