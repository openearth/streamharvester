"""
streamharvester: Harvest streams

Usage:
  streamharvester worker [--broker=BROKER_URL]
  streamharvester beat [--broker=BROKER_URL]
  streamharvester [--broker=BROKER_URL]
  streamharvester -h | --help
  streamharvester --version

Options:
  -h --help             show this help
  --version             show version info
  --url=URL             capture data from this url
  --stream=STREAM       choose the stream [default: best]
  --broker=BROKER_URL   url for celery broker
  --worker              start worker
"""
from __future__ import absolute_import

import os
import pkgutil
import json
import logging
import hashlib

import docopt

from .conventions import basicname

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def set_defaults(options):
    options.update(dict(
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TASK_SERIALIZER='json',
        # Doesn't work for database
        # CELERY_RESULT_SERIALIZER='json',
        # CELERY_RESULT_BACKEND='rpc://',
        # CELERY_TASK_RESULT_EXPIRES=60,
        # CELERY_RESULT_BACKEND='db+sqlite:///a.sqlite'
    ))

def parse_command_line():
    """parse command line options"""

    # open defaults
    options = docopt.docopt(__doc__)

    use_defaults = (
        not options.get('CONFIGFILE') and not options.get('--url')
    )

    if use_defaults:
        set_defaults(options)
        txt = pkgutil.get_data('streamharvester',
                               'data/defaults.json')
        # update the defaults with more options
        options.update(
            json.loads(txt)
        )


    # config file
    if options.get('<configfile>'):
        with open(
                options['<configfile>']
        ) as f:
            extra_options = json.load(f)
            options.update(extra_options)

    if options.get('--url'):
        # add the url as a new station

        # make sure we have a list of stations
        stations = options.get('stations', [])

        # create a new station if needed
        for station in stations:
            # station found
            if station['id'] == 'live':
                break
        else:
            # if we didn't find a station
            # generate a  key
            m = hashlib.md5()
            m.update(options['--url'])
            station = {
                'id': 'live-' + m.hexdigest(),
                'cameras': []
            }
        # make sure the station has cameras
        cameras = station['cameras']
        idx = len(cameras) + 1
        camera = {
            'id': 'c' + str(idx),
            'url': options['--url'],
            'type': 'livestream'
        }
        if options['--stream']:
            camera['stream'] = options['--stream']
        cameras.append(camera)
        stations.append(station)
        options['stations'] = stations
    if options.get('--broker'):
        options['BROKER_URL'] = options.get('--broker')
    return options

def submit_tasks(options):
    from streamharvester.app import app
    app.config_from_object(options)
    for station in options['stations']:
        for task, args in tasks_per_station(station):
            task.apply_async(args)


def tasks_per_station(station):
    """generate tasks, args per station"""
    for camera in station['cameras']:
        info = {}
        product = station['products'][0]
        info.update(station)
        info.update(camera)
        info.update(product)
        info['station'] = station
        info['camera'] = camera
        from streamharvester.tasks import collect, video
        task = collect
        args = (info, )
        yield task, args
        task = video
        args = (info, )
        yield task, args

def worker(options):
    from streamharvester.app import app
    app.config_from_object(options)
    app.start(['celery', 'worker'])

def scheduler(options):
    from datetime import timedelta
    from streamharvester.app import app
    options['CELERYBEAT_SCHEDULE'] = {
        'add-every-30-seconds': {
            'task': 'streamharvester.tasks.add',
            'schedule': timedelta(seconds=30),
            'args': (16, 16)
        }
    }
    app.config_from_object(options)
    app.start(['celery', 'beat'])

CELERY_TIMEZONE = 'UTC'


def main():
    """run the main program"""
    options = parse_command_line()
    logger.debug('options: %s', options)
    if 'worker' in options and options['worker']:
        worker(options)
    if 'beat' in options and options['beat']:
        scheduler(options)
    else:
        submit_tasks(options)
