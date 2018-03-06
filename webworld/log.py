# -*- coding: utf-8 -*-
"""Logging module for webworld"""

import logging
import sys


def setup_logger(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter('%(levelname)s %(name)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
