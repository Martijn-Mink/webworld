import enum

import matplotlib.pyplot as plt
import numpy as np

from . import perlin

WATER_COLORS = ((54, 110, 140),
                (66, 123, 148),
                (78, 135, 155),
                (106, 143, 161),
                (125, 147, 161),
                (155, 164, 169))

LAND_COLORS = ((121, 136, 90),
               (172, 161, 133),
               (174, 142, 82),
               (177, 129, 57),
               (174, 117, 36),
               (167, 98, 32),
               (165, 72, 19),
               (145, 48, 14))


class Quantity(enum.Enum):
    HEIGHT = 0
    FOOD = 1


class World(object):

    def __init__(self, tiles, water_level):
        self.tiles = tiles
        self.water_level = water_level

    @classmethod
    def from_height_map(cls, height_map, water_level):

        tiles = World.tiles_from_height_map(height_map)
        return World(tiles, water_level)

    @classmethod
    def from_shape(cls, height, width, water_level):

        height_map = perlin.noise_map_from_direct_implementation(height, width)
        tiles = World.tiles_from_height_map(height_map)

        return World(tiles, water_level)

    @staticmethod
    def tiles_from_height_map(height_map):

        # TODO: remove lines
        # Set all height to 0 below water level, and scale heights between 0 and 1
        # height_map[height_map < water_level] = water_level
        # height_map = (height_map - np.amin(height_map)) / (np.amax(height_map) - np.amin(height_map))

        tiles = np.empty_like(height_map, dtype=Tile)

        for i_row in range(height_map.shape[0]):
            for i_column in range(height_map.shape[1]):
                height = height_map[i_row, i_column]
                food = height_map[i_row, i_column]
                tile = Tile(height, food)

                tiles[i_row, i_column] = tile

        return tiles

    def give_map(self, quantity):

        quantity_map = np.empty_like(self.tiles, dtype=float)

        for i_row in range(quantity_map.shape[0]):
            for i_column in range(quantity_map.shape[1]):

                if quantity == Quantity.HEIGHT:
                    quantity_map[i_row, i_column] = self.tiles[i_row, i_column].height
                elif quantity == Quantity.FOOD:
                    quantity_map[i_row, i_column] = self.tiles[i_row, i_column].food
                else:
                    raise NotImplementedError()

        return quantity_map

    def visualize_height_map(self):

        color_map = self.give_height_color_map()

        plt.figure()
        plt.imshow(color_map)
        plt.title("Height map of the world")
        plt.show()

    def give_height_color_map(self):

        height_map = self.give_map(Quantity.HEIGHT)

        assert np.amin(height_map) < self.water_level
        assert self.water_level < np.amax(height_map)

        color_map = np.zeros((*height_map.shape, 3)).astype(np.uint8)

        water_color_boundaries = np.linspace(np.amin(height_map), self.water_level, len(WATER_COLORS) + 1)
        for i_color in range(len(WATER_COLORS)):
            color = WATER_COLORS[i_color]
            start_height = water_color_boundaries[i_color]
            end_height = water_color_boundaries[i_color + 1]
            indices = np.logical_and(start_height <= height_map, height_map <= end_height)
            color_map[indices] = color

        land_color_boundaries = np.linspace(self.water_level, np.amax(height_map), len(LAND_COLORS) + 1)
        for i_color in range(len(LAND_COLORS)):
            color = LAND_COLORS[i_color]
            start_height = land_color_boundaries[i_color]
            end_height = land_color_boundaries[i_color + 1]
            indices = np.logical_and(start_height <= height_map, height_map <= end_height)
            color_map[indices] = color

        return color_map


class Tile(object):

    def __init__(self, height, food):
        self.height = height
        self.food = food


def main():
    pass


if __name__ == "__main__":
    main()
