import numpy as np
import noise


def give_noise_map(height, width, octaves=2, lacunarity=0.15, persistence=5):
    noise_map = np.zeros((height, width))

    # TODO: 0.5 offsets are needed, but their precise effect is unclear
    for i_row in range(height):
        for i_column in range(width):
            noise_map[i_row, i_column] = noise.pnoise2(i_row + 0.5, i_column + 0.5, octaves=octaves,
                                                       lacunarity=lacunarity, persistence=persistence)

    return noise_map
