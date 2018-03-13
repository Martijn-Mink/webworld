"""Simple script to display the perlin noise maps with default parameters"""

import matplotlib.pyplot as plt
import numpy as np

import webworld.perlin


def main():
    height = 80
    width = 80

    # External result
    noise_map = webworld.perlin.noise_map_from_external(height, width)
    plt.figure()
    plt.imshow(noise_map)
    plt.title("From external noise module")

    # Direct result
    noise_map, maps_dict = webworld.perlin.noise_map_from_direct_implementation(height, width, return_maps_dict=True)
    plt.figure()
    plt.imshow(noise_map)
    plt.title("From direct implementation")

    # Separate contributions
    plt.figure()
    subplot_index = 1
    for grid_size, noise_map in maps_dict.items():
        subplot_size = np.ceil(np.sqrt(len(maps_dict)))

        plt.subplot(subplot_size, subplot_size, subplot_index)
        subplot_index += 1

        plt.imshow(noise_map)
        plt.title("Gridsize {}".format(grid_size))
        plt.colorbar()

    plt.suptitle("Contibutions from different grid sizes")
    plt.show()


if __name__ == "__main__":
    main()
