import dataclasses


CLOUD_DENSITY_RAIN_THRESHOLD = 5


@dataclasses.dataclass
class State:
    height: int
    temperature: int
    pollution: int
    cloud_density: int

    @property
    def is_raining(self):
        return self.cloud_density >= CLOUD_DENSITY_RAIN_THRESHOLD


