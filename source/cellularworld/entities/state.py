import dataclasses


BASE_RAIN_THRESHOLD = 5
TEMPERATURE_EFFECT_ON_RAIN_FACTOR_WEIGHT = 1
RAIN_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 1
RAIN_EFFECT_ON_POLLUTION_FACTOR_WEIGHT = 1
RAIN_CLOUD_DENSITY_REDUCTION_RATE = 1
TEMPERATURE_EFFECT_ON_POLLUTION_FACTOR_WEIGHT = 0.1
POLLUTION_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 0.1
CLOUD_DENSITY_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 0.1
MAX_CLOUD_EFFECT_ON_TEMPERATURE = 0.5
SUN_EFFECT = 0.1


@dataclasses.dataclass
class State:
    temperature: int = 1
    pollution: int = 0
    cloud_density: int = 1

    def is_raining(self):
        rain_threshold = BASE_RAIN_THRESHOLD + max(0, self.temperature * TEMPERATURE_EFFECT_ON_RAIN_FACTOR_WEIGHT)
        return self.cloud_density >= rain_threshold

    def do_cycle(self):
        self.temperature += SUN_EFFECT / max(1, self.cloud_density)
        self.pollution += self.temperature * TEMPERATURE_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self.temperature += self.pollution * POLLUTION_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
        if not self.is_raining():
            return
        self.temperature -= RAIN_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
        self.pollution -= RAIN_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self.cloud_density -= RAIN_CLOUD_DENSITY_REDUCTION_RATE

    def validate_values(self):
        self.cloud_density = max(0, self.cloud_density)
        self.pollution = max(0, self.pollution)
