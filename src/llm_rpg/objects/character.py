from llm_rpg.llm.llm import LLM
from llm_rpg.scenes.battle.battle_log import BattleLog


class Stats:
    def __init__(self, attack: int, defense: int, focus: int, hp: int):
        # scales damage inflicted
        self.attack = attack
        # reduces damage taken
        self.defense = defense
        # determines amount of letters you can type
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
    def __init__(self, name: str, description: str, stats: Stats):
        super().__init__(name, description, stats)

    def get_next_action(self):
        return input("What is your next action? ")


class Enemy(Character):
    def __init__(self, name: str, description: str, stats: Stats, llm: LLM):
        super().__init__(name, description, stats)
        self.llm = llm

    def get_next_action(self, battle_log: BattleLog, hero: Hero):
        battle_log_text = battle_log.to_string(perspective="enemy")

        prompt = f"""
        You are a video game character that is in a battle against an enemy.
        Try to come up with a natural action based on the battle history.
        Don't repeat the same action every turn.
        
        You have the following description:
        {self.description}

        The enemy has the following description:
        {hero.description}

        Current battle history:
        {battle_log_text}

        Describe your next action very briefly in third person like a narrator would.
        """

        print(prompt)

        return self.llm.generate_completion(prompt)
