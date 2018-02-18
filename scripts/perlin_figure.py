"""Simple script to display the perlin noise map with default parameters"""

import webworld.perlin
import matplotlib.pyplot as plt  # TODO: why is this an unused import?


def main():
    import matplotlib.pyplot as plt

    height = 100
    width = 200
    noise_map = webworld.perlin.give_noise_map(height, width)

    plt.figure()
    plt.imshow(noise_map)
    plt.show()


if __name__ == "__main__":
    main()
