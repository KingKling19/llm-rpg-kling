class Stats:
    def __init__(self, attack: int, defense: int, focus: int, max_hp: int):
        self.attack = attack
        # reduces damage taken
        self.defense = defense
        # determines amount of letters you can type
        self.focus = focus
        # determines how much damage you can take
        self.max_hp = max_hp


class Character:
    def __init__(self, name: str, description: str, level: int, base_stats: Stats):
        # name of the character
        self.name = name
        # description of the character, also includes the items they have equipped
        self.description = description
        # level of the character
        self.level = level
        # stats of the character before any items are equipped
        self.base_stats = base_stats
        # current hp of the character
        self.hp = base_stats.max_hp

    def inflict_damage(self, damage: int):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_dead(self) -> bool:
        return self.hp <= 0

    def full_heal(self):
        self.hp = self.base_stats.max_hp
