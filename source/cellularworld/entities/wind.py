import math
import numpy
import copy
from cellularworld.config import config
import random

RELATIVE_DIRECTION_ANGLE_FACTOR = 45
ZERO_DIRECTION = numpy.array([1., 0.])


class Wind:
    def __init__(self, cell):
        self._cell = cell
        wind = [3., 4.]#[random.uniform(3, 4), random.uniform(3, 4)]
        self._strength = numpy.array(wind)
        self.future_strength = numpy.array(wind)

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

    def unit_vector(self, vector):
        magnitude = numpy.linalg.norm(vector)
        if magnitude == 0:
            return numpy.array([0., 0.])
        return vector / magnitude

    def do_cycle(self):
        self._blow_things_away()
        self._go_with_the_flow()

    def commit(self):
        self._strength = copy.deepcopy(self.future_strength)

    def _blow_things_away(self):
        strength = self.strength_magnitude()
        self._cell.future_state.pollution -= strength * config.effects.elements.wind.on.pollution
        self._cell.future_state.temperature -= strength * config.effects.elements.wind.on.heat
        self._cell.future_state.cloud_density -= strength * config.effects.elements.wind.on.clouds

    def _go_with_the_flow(self):
        self.future_strength = numpy.array([0., 0.])
        for index, neighbour in enumerate(self._cell.neighbours):
            neighbour_effect, dissipation_factor = self._neighbour_effect(index, neighbour.wind)
            neighbour_effect_magnitude = numpy.linalg.norm(neighbour_effect)
            unit_vector = self.unit_vector(neighbour_effect)
            self.wind_heat_interactions(neighbour, unit_vector)
            if neighbour_effect_magnitude == 0 and dissipation_factor == 0:
                continue
            self.affect_wind(dissipation_factor, neighbour, neighbour_effect, unit_vector)
            self.affect_elements(dissipation_factor, neighbour, neighbour_effect_magnitude)

    def wind_heat_interactions(self, neighbour, unit_vector):
        temperature_difference = neighbour.state.temperature - self._cell.state.temperature
        I_AM_HOTTER = temperature_difference < 0
        if I_AM_HOTTER:
            self.future_strength += unit_vector * (abs(temperature_difference) * config.effects.elements.heat.on.wind)
        else:
            self.future_strength -= unit_vector * (temperature_difference * config.effects.elements.heat.on.wind)

    def affect_wind(self, dissipation_factor, neighbour, neighbour_effect, unit_vector):
        self.future_strength += neighbour_effect
        if neighbour.height > config.world.terrain.water_level or self._cell.height > config.world.terrain.water_level:
            self.future_strength += unit_vector * ((neighbour.height - self._cell.height) * config.effects.elements.height.on.wind) * dissipation_factor

    def affect_elements(self, dissipation_factor, neighbour, neighbour_effect_magnitude):
        cooling_amount = (neighbour.state.temperature - self._cell.state.temperature) * neighbour_effect_magnitude
        self._cell.future_state.temperature += cooling_amount * dissipation_factor * config.effects.elements.wind.on.heat
        self._cell.future_state.pollution += neighbour_effect_magnitude * neighbour.state.pollution * dissipation_factor * config.effects.elements.wind.on.pollution
        self._cell.future_state.cloud_density += neighbour_effect_magnitude * neighbour.state.cloud_density * dissipation_factor * config.effects.elements.wind.on.clouds

    def _neighbour_effect(self, neighbour_index, wind):
        my_relative_direction = neighbour_index * RELATIVE_DIRECTION_ANGLE_FACTOR
        my_dissipation_factor = self._dissipation_factor(my_relative_direction, wind.direction)
        if my_dissipation_factor == 0:
            return 0, 0
        normalised_dissipation_factor = self._my_normalised_dissipation_factor(my_dissipation_factor, my_relative_direction, wind)
        neighbour_effect = wind.strength * normalised_dissipation_factor * config.effects.elements.wind.travel_dissipation
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
        if abs(location_direction - wind_direction) > (config.effects.elements.wind.dissipation_cone / 2):
            return 0
        dissipation_factor = math.pow(math.cos(2 * (location_direction - wind_direction)), config.effects.elements.wind.dissipation_limiter)
        return dissipation_factor

    @property
    def direction(self):
        if all(self.strength == 0):
            return 0
        normalised_strength = self.unit_vector(self.strength)
        dot_product = numpy.dot(normalised_strength, ZERO_DIRECTION)
        radians = numpy.arccos(dot_product)
        degrees = numpy.rad2deg(radians)
        if normalised_strength[1] < 0:
            degrees += 180
        return degrees
