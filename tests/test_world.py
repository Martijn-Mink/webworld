import unittest
import lib.world


class TestWorldModule(unittest.TestCase):

    def test_tile(self):
        height = 1
        food = 2

        tile = lib.world.Tile(height=height, food=food)

        self.assertEqual(tile.height, height)
        self.assertEqual(tile.food, food)


if __name__ == '__main__':
    unittest.main()
