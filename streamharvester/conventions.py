import string
import re
import logging

import dateutil.parser

import mako.template

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


verbose_name = re.compile(
    r'(?P<timestamp>\d+)'   # timestamp
    r'\.'
    r'(?P<weekday>\w+)'     # short day
    r'\.'
    r'(?P<month>\w+)'       # short month
    r'\.'
    r'(?P<day>\d+)'         # day
    r'_'
    r'(?P<hour>\d+)'        # hours
    r'_'
    r'(?P<minute>\d+)'      # minutes
    r'_'
    r'(?P<second>\d+)'      # seconds
    r'\.'
    r'(?P<tz>\w+)'          # time zone
    r'\.'
    r'(?P<year>\d+)'        # year
    r'\.'
    r'(?P<station>\w+)'     # station
    r'\.'
    r'c(?P<camera>[\dx]+)'  # camera
    r'\.'
    r'(?P<imgtype>\w+)'     # image type
    r'(\.product_(?P<product>\d+))?'  # [optional] product
    r'\.'
    r'(?P<extension>\w+)'   # extension
)


def generate_filename_verbose(info):
    """generate a filename based on the convention"""
    date_fmt = "%a.%b.%d_%H_%M_%S.%Z.%Y"
    variables = {}

    variables['date'] = dateutil.parser.parse(info['t']).strftime(date_fmt)
    variables.update(info)
    filename_template = "$date.$station.$camera.$imgtype"
    if 'product' in info:
        filename_template += '.product_$product'
        filename_template += '.$extension'
        template = string.Template(filename_template)
        filename = template.substitute(variables)
    return filename

basicname = re.compile(
    r'(?P<station>\w+)'    # station
    r'_'                   # separator
    r'(?P<camera>[\w\d]+)'  # camera
    r'_'                   # separator
    r'(?P<year>\d{4})'   # year
    r'-'                 # separator
    r'(?P<month>\d{2})'  # month
    r'-'
    r'(?P<day>\d{2})'         # day
    r'T'
    r'(?P<hour>\d{2})'        # hours
    r':'
    r'(?P<minute>\d{2})'      # minutes
    r':'
    r'(?P<second>\d{2}(\.[\d]+)?)'      # seconds
    r'(?P<tz>(Z|[+-]\d{2}:\d{2}))?'          # time zone
    r'\.'                  # extension separator
    r'(?P<extension>\w+)'  # day
)

def generate_filename_basic(info):
    """generate a filename based on the convention"""

    # Store images based on an easy to grep filename
    # id can be a combination of station_camera
    info['id'] = info['station']['id'] + '_' + info['camera']['id']
    filename_template = "${id}"
    if 'product' in info:
        filename_template += '_${product}'
    if 't' in info:
        filename_template += '_${t}'
    if 'extension' in info:
        filename_template += '.${extension}'
    logger.info(filename_template)
    template = mako.template.Template(filename_template)
    filename = template.render(**info)
    return filename



def generate_filename(info, convention='basic'):
    if convention == 'verbose':
        filename = generate_filename_verbose(info)
    elif convention == 'basic':
        filename = generate_filename_basic(info)
    return filename
