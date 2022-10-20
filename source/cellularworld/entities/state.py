from cellularworld.config import config
import dataclasses


@dataclasses.dataclass
class State:
    temperature: int = 0
    pollution: int = 0
    cloud_density: int = 0

    def __post_init__(self):
        self.temperature = config.world.start.temperature
        self.pollution = config.world.start.pollution
        self.cloud_density = config.world.start.clouds

    def is_raining(self):
        rain_threshold = config.thresholds.elements.rain.base + max(0, self.temperature * config.effects.elements.heat.on.rain)
        return self.cloud_density >= rain_threshold

    def do_cycle(self):
        cloud_blockage = max(1, self.cloud_density * config.effects.elements.clouds.on.sun)
        temperature, pollution = self.temperature, self.pollution
        self.temperature += config.effects.elements.sun.on.heat / cloud_blockage
        self.temperature += pollution * config.effects.elements.pollution.on.heat
        self.pollution += temperature * config.effects.elements.heat.on.pollution
        if not self.is_raining():
            return
        self.temperature -= config.effects.elements.rain.on.heat
        self.pollution -= config.effects.elements.rain.on.pollution
        self.cloud_density -= config.effects.elements.rain.on.cloud_reduction * (self.cloud_density / config.effects.elements.rain.on.cloud_reduction)

    def validate_values(self):
        self.cloud_density = max(0, self.cloud_density)
        self.pollution = max(0, self.pollution)
