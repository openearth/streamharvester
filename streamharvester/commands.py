"""
streamharvester: Harvest streams

Usage:
  streamharvester
  streamharvester CONFIGFILE
  streamharvester --url URL [--stream=STREAM]
  streamharvester -h | --help
  streamharvester --version

Options:
  -h --help             show this help
  --version             show version info
  --url=URL             capture data from this url
  --stream=STREAM       choose the stream [default: best]
"""
import pkgutil
import json
import logging
import hashlib

import docopt

from .capture import capture_stations
from .processing import process

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_command_line():
    """parse command line options"""

    # open defaults
    options = docopt.docopt(__doc__)

    use_defaults = (
        not options.get('CONFIGFILE') and not options.get('--url')
    )

    if use_defaults:
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

    return options


def main():
    """run the main program"""
    options = parse_command_line()
    logger.debug('options', options)

    logger.debug('analysing stations: %s', options['stations'])
    for img, info in capture_stations(options['stations']):
        process(img, info)
