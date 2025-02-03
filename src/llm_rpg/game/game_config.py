import yaml

from llm_rpg.objects.character import Stats
from llm_rpg.systems.battle.damage_calculator import DamageCalculationConfig
from llm_rpg.systems.battle.enemy_scaling import (
    EnemyArchetypesLevelingAttributeProbs,
    LevelScaling,
    LevelingAttributeProbs,
)


class GameConfig:
    def __init__(self, config_path: str):
        with open(config_path, "r") as file:
            self.game_config = yaml.safe_load(file)

    @property
    def debug_mode(self) -> bool:
        return self.game_config["debug_mode"]

    @property
    def llm_model(self) -> str:
        return self.game_config["llm_model"]

    @property
    def hero_base_stats(self) -> Stats:
        return Stats(
            attack=self.game_config["hero"]["base_hero_stats"]["attack"],
            defense=self.game_config["hero"]["base_hero_stats"]["defense"],
            focus=self.game_config["hero"]["base_hero_stats"]["focus"],
            max_hp=self.game_config["hero"]["base_hero_stats"]["max_hp"],
        )

    @property
    def hero_stats_level_up_amount(self) -> int:
        return self.game_config["hero"]["stats_level_up_amount"]

    @property
    def enemy_level_scaling(self) -> LevelScaling:
        return LevelScaling(
            exp_growth_rate=self.game_config["enemy"]["enemy_level_scaling"][
                "exp_growth_rate"
            ],
            linear_growth_rate=self.game_config["enemy"]["enemy_level_scaling"][
                "linear_growth_rate"
            ],
            linear_scaling_factor=self.game_config["enemy"]["enemy_level_scaling"][
                "linear_scaling_factor"
            ],
        )

    @property
    def enemy_stats_level_up_amount(self) -> int:
        return self.game_config["enemy"]["stats_level_up_amount"]

    @property
    def enemy_leveling_stats_probs(
        self,
    ) -> EnemyArchetypesLevelingAttributeProbs:
        return EnemyArchetypesLevelingAttributeProbs(
            attacker=LevelingAttributeProbs(
                attack=self.game_config["enemy"]["leveling_stats_probs"]["attacker"][
                    "attack"
                ],
                defense=self.game_config["enemy"]["leveling_stats_probs"]["attacker"][
                    "defense"
                ],
                max_hp=self.game_config["enemy"]["leveling_stats_probs"]["attacker"][
                    "max_hp"
                ],
            ),
            defender=LevelingAttributeProbs(
                attack=self.game_config["enemy"]["leveling_stats_probs"]["defender"][
                    "attack"
                ],
                defense=self.game_config["enemy"]["leveling_stats_probs"]["defender"][
                    "defense"
                ],
                max_hp=self.game_config["enemy"]["leveling_stats_probs"]["defender"][
                    "max_hp"
                ],
            ),
            tank=LevelingAttributeProbs(
                attack=self.game_config["enemy"]["leveling_stats_probs"]["tank"][
                    "attack"
                ],
                defense=self.game_config["enemy"]["leveling_stats_probs"]["tank"][
                    "defense"
                ],
                max_hp=self.game_config["enemy"]["leveling_stats_probs"]["tank"][
                    "max_hp"
                ],
            ),
        )

    @property
    def damage_calculation(self) -> DamageCalculationConfig:
        return DamageCalculationConfig(
            attack_scaling=self.game_config["damage_calculator"]["attack_scaling"],
            defense_scaling=self.game_config["damage_calculator"]["defense_scaling"],
            random_factor_max=self.game_config["damage_calculator"][
                "random_factor_max"
            ],
            random_factor_min=self.game_config["damage_calculator"][
                "random_factor_min"
            ],
            llm_dmg_impact=self.game_config["damage_calculator"]["llm_dmg_impact"],
        )

    @property
    def base_enemy_stats(self) -> Stats:
        return Stats(
            attack=self.game_config["enemy"]["base_stats"]["attack"],
            defense=self.game_config["enemy"]["base_stats"]["defense"],
            focus=self.game_config["enemy"]["base_stats"]["focus"],
            max_hp=self.game_config["enemy"]["base_stats"]["max_hp"],
        )

    @property
    def creativity_word_overuse_threshold(self) -> int:
        return self.game_config["creativity_tracker"]["word_overuse_threshold"]
