import math
import numpy
import copy


WIND_EFFECT_ON_POLLUTION_FACTOR_WEIGHT = 1
WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT = 0.1
WIND_EFFECT_ON_CLOUDS_FACTOR_EFFECT = 0.5
HEIGHT_EFFECT_ON_WIND_FACTOR_WEIGHT = 0.1
HEAT_EFFECT_ON_WIND_FACTOR_WEIGHT = 0.1
RELATIVE_DIRECTION_ANGLE_FACTOR = 45
TRAVEL_DISSIPATION = 0.5
DISSIPATION_CONE = 135
DISSIPATION_LIMITER = 2
ZERO_DIRECTION = numpy.array([1., 0.])
UNIT_VECTOR = numpy.array([1., 1.])
SEA_LEVEL = 9


class Wind:
    def __init__(self, cell):
        self._cell = cell
        self._strength = numpy.array([1., 0.])
        self.future_strength = numpy.array([1., 0.])

    def __copy__(self):
        cls = self.__class__
        result = cls(self._cell)
        result._strength = self._strength
        result.future_strength = self.future_strength
        return result

    def __deepcopy__(self, memo):
        return self.__copy__()

    @property
    def strength(self):
        return self._strength

    def strength_magnitude(self):
        return numpy.linalg.norm(self._strength)

    def do_cycle(self):
        self._blow_things_away()
        self._go_with_the_flow()

    def commit(self):
        self._strength = copy.deepcopy(self.future_strength)

    def _blow_things_away(self):
        strength = self.strength_magnitude()
        self._cell.future_state.pollution -= strength * WIND_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self._cell.future_state.temperature -= strength * WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
        self._cell.future_state.cloud_density -= strength * WIND_EFFECT_ON_CLOUDS_FACTOR_EFFECT

    def _go_with_the_flow(self):
        self.future_strength = numpy.array([0., 0.])
        for index, neighbour in enumerate(self._cell.neighbours):
            neighbour_effect, dissipation_factor = self._neighbour_effect(index, neighbour.wind)
            neighbour_effect_magnitude = numpy.linalg.norm(neighbour_effect)
            if neighbour_effect_magnitude == 0 and dissipation_factor == 0:
                continue
            self.affect_wind(dissipation_factor, neighbour, neighbour_effect)
            self.affect_elements(dissipation_factor, neighbour, neighbour_effect_magnitude)
            self.wind_heat_interactions(dissipation_factor, neighbour, neighbour_effect_magnitude)

    def wind_heat_interactions(self, dissipation_factor, neighbour, neighbour_effect_magnitude):
        temperature_difference = neighbour.state.temperature - self._cell.state.temperature
        if temperature_difference < 0:
            self._cell.future_state.temperature += max(-neighbour_effect_magnitude, temperature_difference) * dissipation_factor * WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT
            self.future_strength += temperature_difference * HEAT_EFFECT_ON_WIND_FACTOR_WEIGHT
        else:
            self._cell.future_state.temperature += min(neighbour_effect_magnitude, temperature_difference) * dissipation_factor * WIND_EFFECT_ON_TEMPERATURE_FACTOR_WEIGHT

    def affect_wind(self, dissipation_factor, neighbour, neighbour_effect):
        self.future_strength += neighbour_effect
        if neighbour.height > SEA_LEVEL or self._cell.height > SEA_LEVEL:
            self.future_strength += UNIT_VECTOR * ((neighbour.height - self._cell.height) * HEIGHT_EFFECT_ON_WIND_FACTOR_WEIGHT) * dissipation_factor

    def affect_elements(self, dissipation_factor, neighbour, neighbour_effect_magnitude):
        self._cell.future_state.pollution += min(neighbour_effect_magnitude, neighbour.state.pollution) * dissipation_factor * WIND_EFFECT_ON_POLLUTION_FACTOR_WEIGHT
        self._cell.future_state.cloud_density += min(neighbour_effect_magnitude, neighbour.state.cloud_density) * dissipation_factor * WIND_EFFECT_ON_CLOUDS_FACTOR_EFFECT

    def _neighbour_effect(self, neighbour_index, wind):
        my_relative_direction = neighbour_index * RELATIVE_DIRECTION_ANGLE_FACTOR
        my_dissipation_factor = self._dissipation_factor(my_relative_direction, wind.direction)
        if my_dissipation_factor == 0:
            return 0, 0
        normalised_dissipation_factor = self._my_normalised_dissipation_factor(my_dissipation_factor, my_relative_direction, wind)
        neighbour_effect = wind.strength * normalised_dissipation_factor * TRAVEL_DISSIPATION
        return neighbour_effect, normalised_dissipation_factor

    def _my_normalised_dissipation_factor(self, my_dissipation_factor, my_relative_direction, wind):
        left_neighbour_relative_direction = (my_relative_direction + RELATIVE_DIRECTION_ANGLE_FACTOR)
        right_neighbour_relative_direction = (my_relative_direction - RELATIVE_DIRECTION_ANGLE_FACTOR)
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

    @property
    def direction(self):
        if all(self.strength == 0):
            return 0
        normalised_strength = self.strength / self.strength_magnitude()
        dot_product = numpy.dot(normalised_strength, ZERO_DIRECTION)
        radians = numpy.arccos(dot_product)
        degrees = numpy.rad2deg(radians)
        return degrees
