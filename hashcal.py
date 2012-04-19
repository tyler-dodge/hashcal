#!/usr/bin/python
"""Usage: hashcal.py [options] arguments

Options:
  -h --help         show this help message and exit
  -v --verbose      print status messages
  -q --quiet        print only success or failure
  --version         print the current version
  -a --add          add an item to the list
  -s --show         show all items in the list
  -f --file=<file>  file to store the calendar database in. [default: ~/.hashcal/cal.dat]
"""
from docopt import docopt

import pickle
import os


def main(options, args):
    has_done_something = False
    if options.verbose:
        print args
        print options
        has_done_something = True
    if options.add:
        add_item(options, args)
        has_done_something = True
    if options.show:
        print_items()
        has_done_something = True
    if not has_done_something:
        print __doc__


def add_item(options, args):
    if not os.path.exists(options.file):
        os.makedirs(options.file[:options.file.rfind("/")])
    f = file(options.file, "wb")
    pickle.Pickler(f).dump(args)
    f.close()


def print_items():
    f = file(options.file, "rb")
    print pickle.load(f)
    f.close()


if __name__ == '__main__':
    options, args = docopt(__doc__)
    options.file = os.path.expanduser(options.file)
    main(options, args)
