"""
streamharvester: Harvest streams

Usage:
  streamharvester
  streamharvester CONFIGFILE
  streamharvester --url URL
  streamharvester -h | --help
  streamharvester --version

Options:
  -h --help             show this help
  --version             show version info
  --url=URL             capture data from this url
"""
import pkgutil
import json
import logging

import matplotlib.pyplot as plt

import docopt

from .capture import capture_stations
from .conventions import generate_filename

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

    return options


def main():
    """run the main program"""
    options = parse_command_line()
    if 'stations' in options:
        logger.debug('analysing stations: %s', options['stations'])
        for img, info in capture_stations(options['stations']):
            filename = generate_filename(info)
            plt.imsave(filename, img)
