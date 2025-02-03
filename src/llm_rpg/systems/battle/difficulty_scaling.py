from math import floor
import random
from llm_rpg.objects.character import StatTypes, Stats
from llm_rpg.systems.battle.enemy import Enemy, EnemyArchetypes


def _get_enemy_scaled_level(battles_won: int) -> int:
    # scaling parameters
    EXP_GROWTH_RATE = 1.2
    LINEAR_GROWTH_RATE = 0.6
    LINEAR_SCALING_FACTOR = 0.8
    EXPONENTIAL_SCALING_FACTOR = 1 - LINEAR_SCALING_FACTOR

    # prevent division by zero
    progress = battles_won + 1

    # hybrid stat scaling
    linear_scaled_stat = LINEAR_GROWTH_RATE * progress
    exponential_scaled_stat = EXP_GROWTH_RATE**progress

    total_scaled_stat = floor(
        linear_scaled_stat * LINEAR_SCALING_FACTOR
        + exponential_scaled_stat * EXPONENTIAL_SCALING_FACTOR
    )

    return total_scaled_stat


# TODO volgens mij moet ik enkel het level scalen en dan de stats aanpassen op dezelfde
# manier als de player kan levelen anders wordt het weel heel unbalanced.
# https://docs.google.com/spreadsheets/d/14I8oCT2y5gIoAUscMBXvJAy1lADq-boE7A8sacmtsow/edit?gid=0#gid=0


def scale_enemy(enemy: Enemy, battles_won: int) -> Enemy:
    enemy_level = _get_enemy_scaled_level(battles_won)

    archetype_to_leveling_attribute_probs = {
        EnemyArchetypes.ATTACKER: {
            StatTypes.ATTACK: 0.7,
            StatTypes.DEFENSE: 0.2,
            StatTypes.MAX_HP: 0.1,
        },
        EnemyArchetypes.DEFENDER: {
            StatTypes.ATTACK: 0.1,
            StatTypes.DEFENSE: 0.7,
            StatTypes.MAX_HP: 0.2,
        },
        EnemyArchetypes.TANK: {
            StatTypes.ATTACK: 0.1,
            StatTypes.DEFENSE: 0.2,
            StatTypes.MAX_HP: 0.7,
        },
    }

    leveling_attribute_probs = archetype_to_leveling_attribute_probs[enemy.archetype]

    stat_level_up_amount = 5

    for _ in range(enemy_level):
        stat_type = random.choices(
            list(leveling_attribute_probs.keys()),
            list(leveling_attribute_probs.values()),
        )[0]
        enemy.level_up(stat_type=stat_type, amount=stat_level_up_amount)
