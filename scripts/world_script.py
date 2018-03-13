"""Simple script to generate and display a world object, or write it to the wiki"""

import webworld.log
import webworld.wiki
import webworld.world


def main():
    webworld.log.setup_logger()
    height = 500
    width = 500
    water_level = 0.6
    world = webworld.world.World.from_shape(height, width, water_level)

    # world.visualize_height_map()
    webworld.wiki.create_page(world)


if __name__ == "__main__":
    main()
