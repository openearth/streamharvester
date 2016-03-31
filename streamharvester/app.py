from __future__ import absolute_import

import logging
from celery import Celery

from .capture import capture_stations
from .processing import process

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Celery(
    'harvester',
    include=['streamharvester.tasks']
)


def collect():
    """collecting image"""
    logger.info("collecting image")
