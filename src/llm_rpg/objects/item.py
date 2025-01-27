class StatBoost:
    def __init__(self, attack: int, defense: int, focus: int, hp: int):
        self.attack = attack
        self.defense = defense
        self.focus = focus
        self.hp = hp


class Item:
    def __init__(
        self,
        name: str,
        description: str,
        cost: int,
        stat_boost: StatBoost,
        rarity: int,
    ):
        self.name = name
        self.description = description
        self.cost = cost
        self.stat_boost = stat_boost
        self.rarity = rarity


SWORD = Item(
    name="Sword",
    description="A sword that can cut through anything. Increases attack by 10.",
    cost=100,
    stat_boost=StatBoost(attack=10, defense=0, focus=0, hp=0),
    rarity=1,
)

SHIELD = Item(
    name="Shield",
    description="A shield that can block anything. Increases defense by 10.",
    cost=100,
    stat_boost=StatBoost(attack=0, defense=10, focus=0, hp=0),
    rarity=1,
)

CRYSTAL = Item(
    name="Focus Crystal",
    description="A mystical crystal that enhances mental clarity and concentration. Increases focus by 10.",
    cost=100,
    stat_boost=StatBoost(attack=0, defense=0, focus=10, hp=0),
    rarity=1,
)
