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
import tokenize
import pickle
import os

class HashCal(object):
    def __init__(self, sourceFile=None):
        if sourceFile is not None:
            self.load_from_file(sourceFile)
        else:
            self.events = []
    def find_hashtags(self, args):
        tags = []
        for element in args:
            for token in element.split(" "):
                if token[0] == '#':
                    tags.append(token[1:])
        return tags

    def add_item(self, options, args):
        self.events.append(" ".join(args))

    def load_from_file(self, file_name):
        f = file(file_name, "rb")
        self.events = pickle.load(f)
        f.close()

    def save_to_file(self, file_name):
        if not os.path.exists(file_name):
            os.makedirs(options.file[:file_name.rfind("/")])
        f = file(file_name, "wb")
        pickle.Pickler(f).dump(self.events)
        f.close()
        
    def print_items(self):
        print self.events

def main(options, args):
    has_done_something = False
    calendar = HashCal(options.file)
    if options.verbose:
        print args
        print options
        has_done_something = True
        print calendar.find_hashtags(args)
    if options.add:
        calendar.add_item(options, args)
        calendar.save_to_file(options.file)
        has_done_something = True
    if options.show:
        calendar.print_items()
        has_done_something = True
    if not has_done_something:
        print __doc__


if __name__ == '__main__':
    options, args = docopt(__doc__)
    options.file = os.path.expanduser(options.file)
    main(options, args)
