from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict
from llm_rpg.systems.battle.enemy import Enemy, EnemyArchetypes

if TYPE_CHECKING:
    from llm_rpg.game.game import Game


@dataclass
class BaseEnemyInfo:
    name: str
    description: str
    archetype: EnemyArchetypes
    ascii_render: str


rat = BaseEnemyInfo(
    name="Rat",
    description="A small, scurrying rodent with sharp teeth and a quick bite",
    archetype=EnemyArchetypes.ATTACKER,
    ascii_render="""
(\__/)
(o'.'o)
(")_(")
""",
)

mall_cop = BaseEnemyInfo(
    name="Mall Cop",
    description="Overweight mall cop on a segway, looking for trouble.",
    archetype=EnemyArchetypes.TANK,
    ascii_render="""
      (o_o)
     ⎛( - )⎞
     /(---)\
      || ||
    _/     \_
   (_______)
    O     O
""",
)

angry_bus = BaseEnemyInfo(
    name="Angry Bus",
    description="A bus which gained sentience and is now angry",
    archetype=EnemyArchetypes.TANK,
    ascii_render="""
        __
 ______|_|_____
||  [__]  [__]  |
||__[__]__[__]__|
  o-o       o-o
    """,
)


bear = BaseEnemyInfo(
    name="Bear",
    description="A large, lumbering bear with sharp claws and a powerful roar",
    archetype=EnemyArchetypes.DEFENDER,
    ascii_render="""
    (()__(())
    /       \   
( /    \  \  
    \ o o    /  
    (_()_)__/ \  
/  _.-' /    
/_/     /  
""",
)


robert = BaseEnemyInfo(
    name="Robert",
    description="A robot which can shoot laser from it's eyes",
    archetype=EnemyArchetypes.DEFENDER,
    ascii_render="""
        ,     ,
       (\____/)
        (_oo_)
          (O)
       __||__||__
   []/          \[]
   / \          / \
    /   \________/   \
    (____)        (____)
    """,
)

wellfed_zombie = BaseEnemyInfo(
    name="Wellfed Zombie",
    description="Zombie with an insatiable appetite",
    archetype=EnemyArchetypes.TANK,
    ascii_render="""
         ______
       /      \
      |         | 
      |  ()  () | 
      |    ∩    | 
       \  ---  /  
      /|  |  | |\
     / |       | \
    /  |  ᕕ( ᐛ )ᕗ  | \
   |   |       |   |
   |   |       |   |
   |   \_______/   |
   |               |
   \_____/ \_____/
    (_/       \_)
""",
)

mailbox = BaseEnemyInfo(
    name="Mailbox",
    description="A strong metal mailbox which can attack by shooting letters",
    archetype=EnemyArchetypes.DEFENDER,
    ascii_render="""
      _______
     |       |
     |  ___  |
     | [___] |
     |_______|
    //     \\
   //       \\
  ||         ||
  ||_________||
    | |   | |
    | |   | |

""",
)

conspiracy_theorist = BaseEnemyInfo(
    name="Conspiracy Theorist",
    description="Doesn't believe in anything, even in his own mortality",
    archetype=EnemyArchetypes.ATTACKER,
    ascii_render="""
        .-"      "-.
       /            \
      |              |
      |,  .-.  .-.  ,|
      | )(_o/  \o_)( |
      |/     /\     \|
      (_     ^^     _)
       \__|IIIIII|__/
        | \IIIIII/ |
        \          /
         `--------`
       / ~~~~~~~~ \
      / | | | | | | \
     /  | | | | | |  \
     \  | | | | | |  /
      `~~~~~~~~~~~~`

     "They're watching us..."
""",
)


zephyros = BaseEnemyInfo(
    name="Zephyros",
    description="A cunning and ancient dragon with scales that shimmer like the night sky",
    archetype=EnemyArchetypes.ATTACKER,
    ascii_render="""
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
""",
)

battles_won_to_enemies_mapping: Dict[int, BaseEnemyInfo] = {
    0: rat,
    1: mall_cop,
    2: angry_bus,
    3: bear,
    4: robert,
    5: wellfed_zombie,
    6: mailbox,
    7: conspiracy_theorist,
    8: zephyros,
}


def generate_enemy(game: Game) -> Enemy:
    battles_won = game.battles_won
    enemy_info = battles_won_to_enemies_mapping[battles_won]
    return Enemy(
        name=enemy_info.name,
        description=enemy_info.description,
        level=1,
        base_stats=game.config.base_enemy_stats,
        llm=game.llm,
        enemy_next_action_prompt=game.config.enemy_next_action_prompt,
        archetype=enemy_info.archetype,
        ascii_render=enemy_info.ascii_render,
    )
