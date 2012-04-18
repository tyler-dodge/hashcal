"""Usage: hashcal.py [options] arguments

Options:
  -h --help       show this help message and exit
  -h --verbose    print status messages
  -q --quiet      print only success or failure
"""
from docopt import docopt

def main(options, arguments):
    pass

if __name__ == '__main__':
    options, arguments = docopt(__doc__)
    main(options,arguments)
