"""Determine perlin noise maps. We provide both a wrapper for an implemenation from the external noise module, and also
a direct implementation"""
import logging

import noise
import numpy as np

LOGGER = logging.getLogger(__name__)


def scale_map(noise_map):
    return (noise_map - np.amin(noise_map)) / (np.amax(noise_map) - np.amin(noise_map))


def noise_map_from_external(height, width, octaves=2, lacunarity=0.15, persistence=5):
    noise_map = np.zeros((height, width))

    octaves = int(octaves)

    for i_row in range(height):
        for i_column in range(width):
            noise_map[i_row, i_column] = noise.pnoise2(i_row + 0.5, i_column + 0.5, octaves=octaves,
                                                       lacunarity=lacunarity, persistence=persistence)

    LOGGER.info("Created perlin noise map of size {}*{} using external module".format(width, height))

    scaled_map = scale_map(noise_map)
    return scaled_map


def noise_map_from_direct_implementation(height, width, grid_size_count=9, grid_size_start=3, return_maps_dict=False):
    """Determine a perlin noise map via a direct implementation. following pseudo code in
    https://en.wikipedia.org/wiki/Perlin_noise.

    The implementation calculates a grid of randomly oriented unit vectors. Then, the noise is determined on a
    collection of query points that lie inside this grid. The contributions for several grid sizes (i.e. frequencies)
    are added.

    :returns    The noise map
                An dictionary with the contribution for each grid_size (if return_maps_dict)
    """

    grid_size_count = int(grid_size_count)
    grid_size_start = int(grid_size_start)

    query_length_x = width
    query_length_y = height
    np.random.seed(0)

    # Some arbitrary incommensurate (with 1) values to prevent to linspace values from becoming integers
    coordinate_delta_start = 0.13
    coordinate_delta_end = 0.38

    # Define grid sizes and weights with which they are added. An arbitrary choice is made which results in a good
    # result. Possible improvement is defining separate x and y sizes.
    grid_sizes = np.logspace(np.log10(grid_size_start), np.log10(max(query_length_x, query_length_y)),
                             grid_size_count).astype(int)
    grid_weights = 1 / np.sqrt(grid_sizes)

    # Initialize the result objects
    maps_dict = {}
    maps_array = np.empty((query_length_y, query_length_x, len(grid_sizes)))

    for i_size, (grid_size, grid_weight) in enumerate(zip(grid_sizes, grid_weights)):
        # Calculate the query coordinates
        query_vector_x = np.linspace(coordinate_delta_start, grid_size - 1 - coordinate_delta_end, query_length_x)
        query_vector_y = np.linspace(coordinate_delta_start, grid_size - 1 - coordinate_delta_end, query_length_y)
        query_matrix_x, query_matrix_y = np.meshgrid(query_vector_x, query_vector_y)

        # Determine the noise map for this grid size
        perlin_noise = _PerlinNoiseGrid(grid_size, grid_size)
        noise_map = grid_weight * perlin_noise.compute(query_matrix_x, query_matrix_y)

        # Save the result
        maps_dict[grid_size] = noise_map
        maps_array[:, :, i_size] = noise_map

    combined_noise_map = np.sum(maps_array, axis=2)
    scaled_map = scale_map(combined_noise_map)

    LOGGER.info("Created perlin noise map of size {}*{} using direct implementation".format(width, height))
    if return_maps_dict:
        return scaled_map, maps_dict
    else:
        return scaled_map


class _PerlinNoiseGrid:
    """Private class to compute the noise at a collection of query coordinates for a grid size"""

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

        # Determine the unit vectors on the grid
        grid_angles = 2 * np.pi * np.random.rand(size_x, size_y)
        self.grid_vectors_x = np.cos(grid_angles)
        self.grid_vectors_y = np.sin(grid_angles)

    def compute(self, query_x, query_y):
        # Determine the x and y indices of the four unit vector indices neighboring each query point
        query_indices_left_x = np.floor(query_x).astype(int)
        query_indices_right_x = query_indices_left_x + 1
        query_indices_top_y = np.floor(query_y).astype(int)
        query_indices_bottom_y = query_indices_top_y + 1

        assert np.all(np.logical_and(0 <= query_indices_left_x, query_indices_left_x < self.size_x - 1))
        assert np.all(np.logical_and(0 <= query_indices_top_y, query_indices_top_y < self.size_x - 1))

        # Find the four unit vectors for each point
        query_vectors_top_left = np.dstack((
            self.grid_vectors_x[query_indices_top_y, query_indices_left_x],
            self.grid_vectors_y[query_indices_top_y, query_indices_left_x]))

        query_vectors_top_right = np.dstack((
            self.grid_vectors_x[query_indices_top_y, query_indices_right_x],
            self.grid_vectors_y[query_indices_top_y, query_indices_right_x]))

        query_vectors_bottom_left = np.dstack((
            self.grid_vectors_x[query_indices_bottom_y, query_indices_left_x],
            self.grid_vectors_y[query_indices_bottom_y, query_indices_left_x]))

        query_vectors_bottom_right = np.dstack((
            self.grid_vectors_x[query_indices_bottom_y, query_indices_right_x],
            self.grid_vectors_y[query_indices_bottom_y, query_indices_right_x]))

        # Find the four distance vectors for each point
        query_distances_left_x = np.modf(query_x)[0]
        query_distances_right_x = 1 - query_distances_left_x
        query_distances_top_y = np.modf(query_y)[0]
        query_distances_bottom_y = 1 - query_distances_top_y

        query_distances_top_left = np.dstack((query_distances_left_x, query_distances_top_y))
        query_distances_top_right = np.dstack((query_distances_right_x, query_distances_top_y))
        query_distances_bottom_left = np.dstack((query_distances_left_x, query_distances_bottom_y))
        query_distances_bottom_right = np.dstack((query_distances_right_x, query_distances_bottom_y))

        # Determine the inner products
        inner_products_top_left = np.sum(query_distances_top_left * query_vectors_top_left, axis=2)
        inner_products_top_right = np.sum(query_distances_top_right * query_vectors_top_right, axis=2)
        inner_products_bottom_left = np.sum(query_distances_bottom_left * query_vectors_bottom_left, axis=2)
        inner_products_bottom_right = np.sum(query_distances_bottom_right * query_vectors_bottom_right, axis=2)

        # Interpolate
        interpolation_factor_x = 1 - query_distances_left_x
        ifx = interpolation_factor_x
        interpolation_top = ifx * inner_products_top_left + (1 - ifx) * inner_products_top_right
        interpolation_bottom = ifx * inner_products_bottom_left + (1 - ifx) * inner_products_bottom_right

        interpolation_factor_y = 1 - query_distances_top_y
        ify = interpolation_factor_y
        query_result = ify * interpolation_top + (1 - ify) * interpolation_bottom

        return query_result
