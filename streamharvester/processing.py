import logging

import matplotlib.pyplot as plt

from .conventions import generate_filename

logger = logging.getLogger(__name__)


def process(img, info):
    """process the img"""
    filename = generate_filename(info)
    logger.info('store img: %s', filename)
    plt.imsave(filename, img)
