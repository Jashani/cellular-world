import math


WIND_EFFECT_ON_POLLUTION_FACTOR_WEIGHT = 1
WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 1
WIND_EFFECT_ON_CLOUDS_FACTOR_EFFECT = 1
RELATIVE_DIRECTION_ANGLE_FACTOR = 45
DISSIPATION_CONE = 90
DISSIPATION_LIMITER = 3


class Wind:
    def __init__(self, cell, neighbours):
        self._cell = cell
        self._neighbours = neighbours
        self.strength = (0, 0)  # Will be reimplemented as a proper vector class
        self.direction = 0

    def do_cycle(self):
        self._blow_things_away()
        self._go_with_the_flow()

    def _blow_things_away(self):
        self._cell.state.pollution -= self.strength * WIND_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self._cell.state.temperature -= self.strength * WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
        self._cell.state.cloud_density -= self.strength * WIND_EFFECT_ON_CLOUDS_FACTOR_EFFECT

    def _go_with_the_flow(self):
        for index, neighbour in enumerate(self._neighbours):
            self.redirect(index, neighbour.wind)

    def redirect(self, neighbour_index, wind):
        my_relative_direction = neighbour_index * RELATIVE_DIRECTION_ANGLE_FACTOR
        my_dissipation_factor = self._dissipation_factor(my_relative_direction, wind.direction)
        if my_dissipation_factor == 0:
            return
        normalised_dissipation_factor = self._my_normalised_dissipation_factor(my_dissipation_factor, my_relative_direction, wind)
        self.strength += wind.strength * normalised_dissipation_factor

    def _my_normalised_dissipation_factor(self, my_dissipation_factor, my_relative_direction, wind):
        left_neighbour_relative_direction = (my_relative_direction + RELATIVE_DIRECTION_ANGLE_FACTOR) % RELATIVE_DIRECTION_ANGLE_FACTOR
        right_neighbour_relative_direction = (my_relative_direction + RELATIVE_DIRECTION_ANGLE_FACTOR) % RELATIVE_DIRECTION_ANGLE_FACTOR
        left_neighbour_dissipation_factor = self._dissipation_factor(left_neighbour_relative_direction, wind.direction)
        right_neighbour_dissipation_factor = self._dissipation_factor(right_neighbour_relative_direction, wind.direction)
        factor_sum = my_dissipation_factor + left_neighbour_dissipation_factor + right_neighbour_dissipation_factor
        normalised_dissipation_factor = my_dissipation_factor / factor_sum
        return normalised_dissipation_factor

    def _dissipation_factor(self, location_direction, wind_direction):
        if abs(location_direction - wind_direction) > (DISSIPATION_CONE / 2):
            return 0
        dissipation_factor = math.pow(math.cos(2 * (location_direction - wind_direction)), DISSIPATION_LIMITER)
        return dissipation_factor
