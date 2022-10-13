import dataclasses


CLOUD_DENSITY_RAIN_THRESHOLD = 5
BASE_RAIN_THRESHOLD = 5
TEMPERATURE_EFFECT_ON_RAIN_FACTOR_WEIGHT = 5
RAIN_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 1
RAIN_EFFECT_ON_POLLUTION_FACTOR_WEIGHT = 1
RAIN_CLOUD_DENSITY_REDUCTION_RATE = 1


@dataclasses.dataclass
class State:
    temperature: int
    pollution: int
    cloud_density: int

    def is_raining(self):
        rain_threshold = BASE_RAIN_THRESHOLD + max(0, self.temperature * TEMPERATURE_EFFECT_ON_RAIN_FACTOR_WEIGHT)
        return self.cloud_density >= rain_threshold

    def do_cycle(self):
        if not self.is_raining():
            return
        self.temperature -= RAIN_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
        self.pollution -= RAIN_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self.cloud_density -= RAIN_CLOUD_DENSITY_REDUCTION_RATE

