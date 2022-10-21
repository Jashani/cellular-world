import box
import numpy
import random
import tkinter.font
import tkinter as tk
import cellularworld.config
import matplotlib.pyplot as plt
from cellularworld.config import config
from cellularworld.world import matrix
from cellularworld.frontend import unit
from cellularworld.world import terrain, landform
from cellularworld.entities.biome import biome_type

COLOUR_JUMP = 15
COLOUR = {biome_type.BiomeType.CITY: '#ff9500',
          biome_type.BiomeType.FOREST: '#134727',
          biome_type.BiomeType.ICE: '#d0edf2',
          "WHITE": "#ffffff"}


class Simulator:
    def __init__(self):
        cellularworld.config.initialise()
        self._window = tk.Tk()
        self._world = None
        self._text_matrix = None
        self._label_matrix = None
        self._font = tkinter.font.Font(family='Courier New', size=8)
        self._data = box.Box(temperature=[], cloud_density=[], pollution=[], wind=[])

        self._build_world()
        self._build_text_matrix()
        self._render_world()

    def _build_world(self):
        seed = config.world.seed or random.randint(0, 2**16)
        land = landform.Landform()
        _terrain = terrain.Terrain()
        self._world = _terrain.generate(seed)
        land.populate(self._world, seed)
        self._commit_world()

    def _build_text_matrix(self):
        self._text_matrix = matrix.Matrix(self._world.width, self._world.height)
        for row, column in self._text_matrix.all_cells():
            self._text_matrix[row][column] = tkinter.StringVar()
            self._text_matrix[row][column].set('XXXX')

    def _commit_world(self):
        self._world.apply_to_all(lambda cell: cell.commit())

    def _render_world(self):
        self._label_matrix = matrix.Matrix(self._world.width, self._world.height)
        for row, column in self._world.all_cells():
            self._render_cell(row, column)

    def _render_cell(self, row, column):
        frame = tk.Frame(master=self._window, bg='black')
        frame.grid(row=row, column=column)
        full_colour = self._biome_colour(column, row)
        label = tk.Label(master=frame, bg=full_colour, textvariable=self._text_matrix[row][column],
                         font=self._font, fg=COLOUR['WHITE'])
        self._label_matrix[row][column] = label
        label.pack()

    def _biome_colour(self, column, row):
        colour = COLOUR_JUMP * self._world[row][column].height
        hex_colour = hex(colour)[2:].zfill(2)
        full_colour = self._land_or_sea(colour, hex_colour)
        full_colour = COLOUR.get(self._world[row][column].biome.type, full_colour)
        return full_colour

    def _land_or_sea(self, colour, hex_colour):
        if colour <= COLOUR_JUMP * 9:
            return f"#0000{hex_colour}"
        return f"#00{hex_colour}00"

    def run(self):
        print("Running!")
        iterations = 0
        stabilisation_period = config.world.stabilisation_period
        while iterations < config.world.days + stabilisation_period:
            iterations += 1
            print(f"Cycle: {iterations}")
            self._window.update()
            self._cycle()
            self._append_data()
            self._commit_world()
        print(f"Ran {iterations} iterations.")
        self._create_plot(stabilisation_period)

    def _append_data(self):
        averages = self._calculate_averages()
        self._data.cloud_density.append(averages.cloud_density)
        self._data.pollution.append(averages.pollution)
        self._data.wind.append(averages.wind_magnitude)
        self._data.temperature.append(averages.temperature)
        print(f"\tAvg wind: {averages.wind_magnitude}{str(unit.Unit.WIND)} ({averages.wind})"
              f"\n\tAvg temperature: {averages.temperature}{str(str(unit.Unit.TEMPERATURE))}"
              f"\n\tAvg pollution: {averages.pollution}{str(unit.Unit.POLLUTION)}"
              f"\n\tAvg cloud density: {averages.cloud_density}{str(unit.Unit.CLOUD_DENSITY)}")

    def _cycle(self):
        for row, column in self._world.all_cells():
            self._world[row][column].do_cycle()
            presentable = self._label_content(self._world[row][column])
            self._text_matrix[row][column].set(presentable)

    def _label_content(self, cell):
        temperature = ("{:.1f}".format(cell.state.temperature) + str(unit.Unit.TEMPERATURE)).rjust(8)
        pollution = ("{:.1f}".format(cell.state.pollution) + str(unit.Unit.POLLUTION)).rjust(8)
        clouds = ("{:.1f}".format(cell.state.cloud_density) + str(unit.Unit.CLOUD_DENSITY)).rjust(8)
        wind = ("{:.1f}".format(cell.wind.strength_magnitude()) + str(unit.Unit.WIND)).rjust(8)
        direction = ("{:.1f}".format(cell.wind.direction_angle)).rjust(8)
        presentable = "\n".join([temperature, pollution, clouds, wind, direction])
        return presentable

    def _calculate_averages(self):
        averages = box.Box(wind=numpy.array([0., 0.]), temperature=0,
                           wind_magnitude=0, pollution=0, cloud_density=0)
        for row, column in self._world.all_cells():
            averages.wind += self._world[row][column].wind.strength
            averages.wind_magnitude += self._world[row][column].wind.strength_magnitude()
            averages.temperature += self._world[row][column].state.temperature
            averages.pollution += self._world[row][column].state.pollution
            averages.cloud_density += self._world[row][column].state.cloud_density
        averages.wind /= self._world.height * self._world.width
        averages.wind_magnitude /= self._world.height * self._world.width
        averages.temperature /= self._world.height * self._world.width
        averages.pollution /= self._world.height * self._world.width
        averages.cloud_density /= self._world.height * self._world.width
        return averages

    def _create_plot(self, stabilisation_period):
        plt.title(f'City effect on pollution: {config.effects.biomes.city.on.pollution}')
        days = [day + 1 - stabilisation_period for day in range(config.world.days + stabilisation_period)]
        figure, (values, standard) = plt.subplots(2, sharex=True, figsize=(10, 8))
        self._plot_data(self._data, days, values)
        standardised_data = self._standardised_data()
        self._plot_data(standardised_data, days, standard)
        plt.xlabel('Day')
        values.set_ylabel('Value')
        standard.set_ylabel('Standardised Value')
        plt.legend()
        plt.show()

    def _plot_data(self, data, days, values):
        values.axhline(y=0, color='black')
        values.plot(days, data.temperature, label='Temperature')
        values.plot(days, data.pollution, label='Pollution')
        values.plot(days, data.cloud_density, label='Cloud Density')
        values.plot(days, data.wind, label='Wind Magnitude')
        values.axvline(x=0, color='r', label='End of stabilisation period')

    def _standardised_data(self):
        standardised_data = box.Box(temperature=[], cloud_density=[], pollution=[], wind=[])
        standardised_data.temperature = self._standardise(self._data.temperature)
        standardised_data.pollution = self._standardise(self._data.pollution)
        standardised_data.cloud_density = self._standardise(self._data.cloud_density)
        standardised_data.wind = self._standardise(self._data.wind)
        return standardised_data

    def _standardise(self, data):
        average = numpy.average(data)
        standard_deviation = numpy.std(data)
        standardised = [(point - average) / standard_deviation for point in data]
        return standardised


def wait_for_exit():
    while True:
        import time
        time.sleep(1000)


if __name__ == '__main__':
    simulator = Simulator()
    try:
        simulator.run()
        wait_for_exit()
    except KeyboardInterrupt:
        plt.close("all")
        print("Exiting")
        import sys
        sys.exit()
