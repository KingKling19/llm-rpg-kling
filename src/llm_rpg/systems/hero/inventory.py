from typing import List

from llm_rpg.objects.item import Item


class Inventory:
    def __init__(self, max_items: int):
        self.items: List[Item] = []
        self.max_items = max_items

    def add_item(self, item: Item):
        if len(self.items) < self.max_items:
            self.items.append(item)
        else:
            raise ValueError("Inventory is full")

    def remove_item(self, item: Item):
        self.items.remove(item)

    def is_full(self) -> bool:
        return len(self.items) >= self.max_items
