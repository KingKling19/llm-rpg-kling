from dataclasses import dataclass
from llm_rpg.objects.character import Character, Stats
from llm_rpg.objects.item import (
    Item,
)
from llm_rpg.systems.hero.inventory import Inventory
from llm_rpg.utils.timer import Timer


@dataclass
class ProposedHeroAction:
    action: str
    time_to_answer_seconds: float
    is_valid: bool
    invalid_reason: str = None


@dataclass
class HeroClass:
    class_name: str
    description: str
    base_stats: Stats
    starting_item: Item
    ascii_render: str = ""


class Hero(Character):
    def __init__(
        self,
        name: str,
        class_name: str,
        description: str,
        level: int,
        base_stats: Stats,
        max_items: int,
        ascii_render: str = "",
    ):
        super().__init__(
            name=name, description=description, level=level, base_stats=base_stats
        )
        self.class_name = class_name
        self.inventory = Inventory(max_items=max_items)
        self.discovered_item = False
        self.ascii_render = ascii_render

    def dont_pick_up_item(self):
        self.discovered_item = False

    def replace_item_with_discovered_item(
        self, item_to_remove: Item, discovered_item: Item
    ):
        self.inventory.remove_item(item_to_remove)
        self.inventory.add_item(discovered_item)
        self.discovered_item = False

    def pick_up_discovered_item(self, item: Item):
        self.inventory.add_item(item)
        self.discovered_item = False

    def get_current_stats(self) -> Stats:
        # need to make a copy of the base stats because else we are going to modify the base stats
        base_stats = Stats(
            attack=self.base_stats.attack,
            defense=self.base_stats.defense,
            focus=self.base_stats.focus,
            max_hp=self.base_stats.max_hp,
        )
        for item in self.inventory.items:
            base_stats.attack = item.boost_attack(base_stats.attack)
            base_stats.defense = item.boost_defense(base_stats.defense)
            base_stats.focus = item.boost_focus(base_stats.focus)
            base_stats.max_hp = item.boost_max_hp(base_stats.max_hp)
        return base_stats

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
        if n_chars > self.get_current_stats().focus:
            return ProposedHeroAction(
                action="",
                is_valid=False,
                time_to_answer_seconds=timer.interval,
                invalid_reason=f"Your current focus is {self.get_current_stats().focus} which only allows you to type "
                f"{self.get_current_stats().focus} characters. You typed {n_chars} non-whitespace characters. Try again.",
            )
        else:
            return ProposedHeroAction(
                action=proposed_input,
                is_valid=True,
                time_to_answer_seconds=timer.interval,
            )

    def render(self):
        print("")
        print(f"🦸 {self.name} lvl {self.level}")
        print(f"Class: {self.class_name}")
        print(f"Description: {self.description}")
        if self.ascii_render:
            print("")
            print(self.ascii_render)
        print("")
        print(f"HP: {self.get_current_stats().max_hp}")
        print(f"Focus: {self.get_current_stats().focus}")
        print(f"Attack: {self.get_current_stats().attack}")
        print(f"Defense: {self.get_current_stats().defense}")
        print("")
        print("Items:")
        for item in self.inventory.items:
            print(f"  - {item.name}")
        print("")
