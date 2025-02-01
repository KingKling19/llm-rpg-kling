from textwrap import dedent
from llm_rpg.llm.llm import LLM
from llm_rpg.objects.character import Character, Stats
from llm_rpg.systems.hero.hero import Hero
from llm_rpg.systems.battle.battle_log import BattleLog


class Enemy(Character):
    def __init__(self, name: str, description: str, level: int, stats: Stats, llm: LLM):
        super().__init__(name=name, description=description, level=level, stats=stats)
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
        print(f"👾 {self.name} lvl {self.level}")
        print(self.description)
        print(f"HP: {self.stats.hp}")
        print(f"Attack: {self.stats.attack}")
        print(f"Defense: {self.stats.defense}")
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
