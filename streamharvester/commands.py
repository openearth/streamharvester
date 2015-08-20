"""
streamharvester: Harvest streams

Usage:
  streamharvester <configfile>
  streamharvester --url URL
  streamharvester -h | --help
  streamharvester --version

Options:
  -h --help             show this help
  --version             show version info
  --url=URL             capture data from this url
"""
import docopt


def parse_command_line():
    """parse command line options"""
    options = docopt.docopt(__doc__)
    return options


def main():
    """run the main program"""
    options = parse_command_line()
    print(options)
