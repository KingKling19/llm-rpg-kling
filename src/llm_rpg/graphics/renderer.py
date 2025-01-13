from llm_rpg.llm.llm import LLM
from llm_rpg.objects.character import Character


class Renderer:
    def __init__(self, llm: LLM):
        self.llm = llm

    def render_character(self, character: Character):
        # prompt to render character in ascii
        prompt = f"Draw the following character in very simplistic ascii art stick drawing: {character.description}. Only output the ascii, no other text. The ascii should be rather small like 20x20 characters."
        completion = self.llm.generate_completion(prompt)
        print(completion)
