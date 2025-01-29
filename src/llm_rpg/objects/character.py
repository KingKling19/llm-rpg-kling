class Stats:
    def __init__(self, attack: int, defense: int, focus: int, hp: int):
        self.attack = attack
        # reduces damage taken
        self.defense = defense
        # determines amount of letters you can type
        self.focus = focus
        # determines how much damage you can take
        self.max_hp = hp
        self.hp = hp


class Character:
    def __init__(self, name: str, description: str, level: int, stats: Stats):
        # name of the character
        self.name = name
        # description of the character, also includes the items they have equipped
        self.description = description
        # level of the character
        self.level = level
        # stats of the character
        self.stats = stats
