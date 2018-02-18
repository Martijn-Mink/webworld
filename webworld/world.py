import numpy
import enum

from . import perlin


class Quantity(enum.Enum):
    HEIGHT = 0
    FOOD = 1


class World(object):

    def __init__(self, tiles, water_level):
        self.tiles = tiles
        self.water_level = water_level

    @classmethod
    def from_maps(cls, height_map, food_map, water_level):
        assert height_map.shape == food_map.shape

        # Construct tiles
        tiles = numpy.empty_like(height_map, dtype=Tile)

        for i_row in range(height_map.shape[0]):
            for i_column in range(height_map.shape[1]):
                height = height_map[i_row, i_column]
                food = food_map[i_row, i_column]
                tile = Tile(height, food)

                tiles[i_row, i_column] = tile

        return World(tiles, water_level)

    @classmethod
    def from_shape(cls, height, width, water_level):

        noise_map = perlin.give_noise_map(height, width)

        # Construct tiles
        tiles = numpy.empty_like(noise_map, dtype=Tile)

        for i_row in range(noise_map.shape[0]):
            for i_column in range(noise_map.shape[1]):
                height = noise_map[i_row, i_column]
                food = noise_map[i_row, i_column]
                tile = Tile(height, food)

                tiles[i_row, i_column] = tile

        return World(tiles, water_level)

    def give_map(self, quantity):

        quantity_map = numpy.empty_like(self.tiles, dtype=float)

        for i_row in range(quantity_map.shape[0]):
            for i_column in range(quantity_map.shape[1]):

                if quantity == Quantity.HEIGHT:
                    quantity_map[i_row, i_column] = self.tiles[i_row, i_column].height
                elif quantity == Quantity.FOOD:
                    quantity_map[i_row, i_column] = self.tiles[i_row, i_column].food
                else:
                    raise NotImplementedError()

        return quantity_map


class Tile(object):

    def __init__(self, height, food):
        self.height = height
        self.food = food


def main():
    pass


if __name__ == "__main__":
    main()
