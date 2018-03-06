import datetime
import os
import unittest

import matplotlib.image
import numpy as np

import webworld.log
import webworld.wiki

TEST_IMAGE_SIZE = 20
TEMPORARY_IMAGE_PATH = "temporary_image.png"


class TestWikiModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        webworld.log.setup_logger()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEMPORARY_IMAGE_PATH):
            os.remove(TEMPORARY_IMAGE_PATH)

    @staticmethod
    def create_image():
        im = np.uint8(255 * np.random.rand(TEST_IMAGE_SIZE, TEST_IMAGE_SIZE, 3))
        matplotlib.image.imsave(TEMPORARY_IMAGE_PATH, im)

    def test_create_page(self):
        self.create_image()

        title = "Unittest Page"
        summary = "Page created by unittest"
        contents = "This page was created by a unittest on {}.".format(datetime.datetime.now())
        webworld.wiki.write_page(title, contents, image_paths=[TEMPORARY_IMAGE_PATH], summary=summary)


if __name__ == '__main__':
    unittest.main()
