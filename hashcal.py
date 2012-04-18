"""Usage: hashcal.py [options] arguments

Options:
  -h --help       show this help message and exit
  -v --verbose    print status messages
  -q --quiet      print only success or failure
  --version       print the current version
"""
from docopt import docopt

def main(options, arguments):
    pass

if __name__ == '__main__':
    options, arguments = docopt(__doc__, version="Version 0.1")
    main(options,arguments)
