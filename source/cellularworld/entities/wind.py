import math
import numpy
import copy
from cellularworld.entities import vector_tools
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
        return vector_tools.magnitude(self._strength)

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

    def wind_heat_interactions(self, neighbour, towards_me):
        temperature_difference = neighbour.state.temperature - self._cell.state.temperature
        I_AM_HOTTER = temperature_difference < 0
        if I_AM_HOTTER:
            self.future_strength += towards_me * (abs(temperature_difference) * config.effects.elements.heat.on.wind)
        else:
            self.future_strength -= towards_me * (temperature_difference * config.effects.elements.heat.on.wind)

    def affect_wind(self, dissipation_factor, neighbour, neighbour_effect, towards_me):
        self.future_strength += neighbour_effect
        if neighbour.height > self._cell.height:
            self.future_strength += towards_me * ((neighbour.height - self._cell.height) * config.effects.elements.height.on.wind) * dissipation_factor

    def affect_elements(self, dissipation_factor, neighbour, neighbour_effect_magnitude):
        temperature_difference = neighbour.state.temperature - self._cell.state.temperature
        temperature_effect = temperature_difference * neighbour_effect_magnitude * config.effects.elements.wind.on.heat
        pollution_effect = neighbour_effect_magnitude * neighbour.state.pollution * config.effects.elements.wind.on.pollution
        cloud_effect = neighbour_effect_magnitude * neighbour.state.cloud_density * config.effects.elements.wind.on.clouds
        self._cell.future_state.temperature += min(temperature_difference, temperature_effect) * dissipation_factor
        self._cell.future_state.pollution += min(pollution_effect, neighbour.state.pollution) * dissipation_factor
        self._cell.future_state.cloud_density += min(cloud_effect, neighbour.state.cloud_density) * dissipation_factor

    def _neighbour_effect(self, neighbour_index, wind):
        my_relative_direction = neighbour_index * RELATIVE_DIRECTION_ANGLE_FACTOR
        my_dissipation_factor = self._dissipation_factor(my_relative_direction, wind.direction_angle)
        if my_dissipation_factor == 0:
            return 0, 0
        normalised_dissipation_factor = self._my_normalised_dissipation_factor(my_dissipation_factor, my_relative_direction, wind)
        neighbour_effect = wind.strength * normalised_dissipation_factor * config.effects.elements.wind.travel_dissipation
        return neighbour_effect, normalised_dissipation_factor

    def _my_normalised_dissipation_factor(self, my_dissipation_factor, my_relative_direction, wind):
        left_neighbour_relative_direction = (my_relative_direction + RELATIVE_DIRECTION_ANGLE_FACTOR)
        right_neighbour_relative_direction = (my_relative_direction - RELATIVE_DIRECTION_ANGLE_FACTOR)
        left_neighbour_dissipation_factor = self._dissipation_factor(left_neighbour_relative_direction, wind.direction_angle)
        right_neighbour_dissipation_factor = self._dissipation_factor(right_neighbour_relative_direction, wind.direction_angle)
        factor_sum = my_dissipation_factor + left_neighbour_dissipation_factor + right_neighbour_dissipation_factor
        normalised_dissipation_factor = my_dissipation_factor / factor_sum
        return normalised_dissipation_factor

    def _dissipation_factor(self, location_direction, wind_direction):
        if abs(location_direction - wind_direction) > (config.effects.elements.wind.dissipation_cone / 2):
            return 0
        dissipation_factor = math.pow(math.cos(2 * (location_direction - wind_direction)), config.effects.elements.wind.dissipation_limiter)
        return dissipation_factor

    @property
    def direction_angle(self):
        return vector_tools.direction_angle(self.strength)

    def _my_relative_direction(self, neighbour_index):
        return neighbour_index * RELATIVE_DIRECTION_ANGLE_FACTOR

    def _towards_me(self, neighbour_index):
        my_relative_direction = self._my_relative_direction(neighbour_index)
        direction_vector = vector_tools.direction_vector(my_relative_direction)
        return direction_vector
