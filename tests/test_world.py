import unittest
import webworld.world
import numpy as np


class TestWorldModule(unittest.TestCase):

    def test_tile(self):
        height = 1
        food = 2

        tile = webworld.world.Tile(height=height, food=food)

        self.assertEqual(tile.height, height)
        self.assertEqual(tile.food, food)

    def test_world(self):
        # From maps
        size = 5
        input_height_map = np.eye(size)
        input_food_map = 2 * np.eye(size)
        water_level = 0.5
        world = webworld.world.World.from_maps(input_height_map, input_food_map, water_level)
        height_map = world.give_map(webworld.world.Quantity.HEIGHT)
        food_map = world.give_map(webworld.world.Quantity.FOOD)

        self.assertEqual(height_map.shape, input_height_map.shape)
        self.assertEqual(food_map.shape, input_food_map.shape)

        # From shape
        height = 100
        width = 200
        water_level = 0.5
        world = webworld.world.World.from_shape(height, width, water_level)
        height_map = world.give_map(webworld.world.Quantity.HEIGHT)
        food_map = world.give_map(webworld.world.Quantity.FOOD)

        self.assertEqual(height_map.shape, (height, width))
        self.assertEqual(food_map.shape, (height, width))


if __name__ == '__main__':
    unittest.main()
