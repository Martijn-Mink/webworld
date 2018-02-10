"""This script creates a Matplotlib GUI with sliders to explore the dependency of the perlin noise map on it's
parameters."""

import numpy as np
import inspect
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import noise

N_PIXELS = 80
SLIDER_HEIGHT = 0.05
LEFT_MARGIN = 0.1
RIGHT_MARGIN = 0.1
TOP_MARGIN = 0.1
BOTTOM_MARGIN = 0.1


def determine_mpl_axes_extends(fractions):
    """Generate a list of arguments for plt.axes, so that we get vertically aligned parts with heights given by the
    fractions. Margins are also included."""
    fractions = [TOP_MARGIN, *fractions, BOTTOM_MARGIN]
    fractions = [fraction / sum(fractions) for fraction in fractions]
    bottoms = np.cumsum([0, *fractions[:-1]])

    fractions = fractions[1:-1]
    bottoms = bottoms[1:-1]

    left = LEFT_MARGIN
    width = 1 - LEFT_MARGIN - RIGHT_MARGIN
    lbwh_list = [[left, bottom, width, height] for (height, bottom) in zip(fractions, bottoms)]

    return lbwh_list


class Variable(object):
    """A variable that can appear on a slider"""

    def __init__(self, name, min_value, max_value, initial_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.initial_value = initial_value


class DynamicArray(object):
    """An array wrapper that encapsulates data to alter it dynamically. It contains a function to calculate the array,
    the current values of the variables to calculate is (i.e. it has a state), and a convenience function to update
    the value of a variable and recalculate the array"""

    def __init__(self, generating_function, variables):
        signature = inspect.signature(generating_function)
        assert len(signature.parameters) == len(variables)

        self.generating_function = generating_function
        self.variables = variables
        self.n_variables = len(self.variables)

        self.current_values = [variable.initial_value for variable in variables]

    def update_and_calculate(self, i_variable, new_value):
        assert 0 <= i_variable < len(self.variables)
        self.current_values[i_variable] = new_value
        return self.calculate()

    def calculate(self):
        return self.generating_function(*self.current_values)


class DynamicFigure(object):
    """A that handles the dynamic visualization of the dynamic_array. For each variable of the dynamic_array a
    slider is created which is connected to the correct update function of the dynamic_array"""

    def __init__(self, dynamic_array):
        self.dynamic_array = dynamic_array  # type: DynamicArray

        # Determine axes extends
        sliders_height = len(self.dynamic_array.variables) * SLIDER_HEIGHT
        fractions = [1 - sliders_height] + self.dynamic_array.n_variables * [SLIDER_HEIGHT]

        mpl_axes_extends = determine_mpl_axes_extends(fractions)
        self.array_axes_extend = mpl_axes_extends[0]
        self.slider_axes_extends = mpl_axes_extends[1:]

        # Setup figure
        self.figure = plt.figure()

        # Add array axes
        self.array_axes = self.figure.add_axes(self.array_axes_extend)
        self.array_axes.imshow(self.dynamic_array.calculate())

        # Create slider objects and add their axes. We need to save the slider references or they do not work.
        self.sliders = []

        for i_variable, variable in enumerate(self.dynamic_array.variables):
            axes = self.figure.add_axes(self.slider_axes_extends[i_variable])

            slider = Slider(axes, variable.name, variable.min_value, variable.max_value, valinit=variable.initial_value)

            self._set_on_changed_for_slider(slider, i_variable)

            self.sliders.append(slider)

    def _set_on_changed_for_slider(self, slider, i_variable):
        """Method needed to make the i_variable variable local, see
        https://docs.python.org/3/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-
        values-all-return-the-same-result"""
        slider.on_changed(lambda new_value: self.update(i_variable, new_value))

    def update(self, i_variable, new_value):
        """Entry point to be given to slider.on_changed"""

        array = self.dynamic_array.update_and_calculate(i_variable, new_value)

        # Todo alter the image content directly
        self.array_axes.imshow(array)

        self.figure.canvas.draw_idle()


def calculate_noise_map(octaves, lacunarity, persistence):
    """Calculate the perlin noise map"""

    print("{}: {}".format('octaves', octaves))
    print("{}: {}".format('lacunarity', lacunarity))
    print("{}: {}".format('persistence', persistence))

    # TODO: 0.5 offsets are needed, but their precise effect is unclear
    noise_map = np.zeros((N_PIXELS, N_PIXELS))
    for i in range(N_PIXELS):
        for j in range(N_PIXELS):
            noise_map[i, j] = noise.pnoise2(i + 0.5, j + 0.5, octaves=int(octaves), lacunarity=lacunarity,
                                            persistence=persistence)

    return noise_map


def main():
    variables = [Variable('octaves', 2, 10, 2),
                 Variable('lacunarity', 0, 1, 0.15),
                 Variable('persistence', 0, 5, 5)]

    dynamic_array = DynamicArray(calculate_noise_map, variables)
    DynamicFigure(dynamic_array)

    plt.show()


if __name__ == "__main__":
    main()
