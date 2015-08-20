import string
import re

argusname = re.compile(
    r'(?P<timestamp>\d+)' # timestamp
    r'\.'
    r'(?P<weekday>\w+)'   # short day
    r'\.'
    r'(?P<month>\w+)'     # short month
    r'\.'
    r'(?P<day>\d+)'       # day
    r'_'
    r'(?P<hour>\d+)'      # hours
    r'_'
    r'(?P<minute>\d+)'    # minutes
    r'_'
    r'(?P<second>\d+)'    # seconds
    r'\.'
    r'(?P<tz>\w+)'        # time zone
    r'\.'
    r'(?P<year>\d+)'      # year
    r'\.'
    r'(?P<station>\w+)'   # station
    r'\.'
    r'c(?P<camera>[\dx]+)'# camera
    r'\.'
    r'(?P<imgtype>\w+)'   # image type
    r'(\.product_(?P<product>\d+))?' # [optional] product
    r'\.'
    r'(?P<extension>\w+)' # extension
    )

def generate_filename(info):
    """generate a filename based on the convention"""
    date_fmt = "%a.%b.%d_%H_%M_%S.%Z.%Y"
    variables = {}
    variables['date'] = info['t'].strftime(date_fmt)
    variables.update(info)
    filename_template = "$date.$station.$camera.$imgtype"
    if 'product' in info:
        filename_template += '.product_$product'
    filename_template += '.$extension'
    template = string.Template(filename_template)
    filename = template.substitute(variables)
    return filename

