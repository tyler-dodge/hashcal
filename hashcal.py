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

def file_check(fn):
    def wrap(self, file_name, *args):
        directory = file_name[:file_name.rfind("/")]
        if not os.path.exists(directory):
            os.makedirs(directory) #create directory
        if not os.path.exists(file_name):
            file(file_name, "w").close() # create file and close it
        fn(self, file_name, *args)
    return wrap

class HashCal(object):
    def __init__(self, source_file=None):
        """Create HashCal. If file is given, load events from it"""
        if source_file is not None:
            self.load_from_file(source_file)
        else:
            self.events = []
    def split_hashtags(self, args):
        """Given a set of args, will return a tuple of: 
            An array of all the hashtagged args with the hashtags stripped, 
            and an array of all the args without hashtags."""
        tag_args = []
        notag_args = []
        for element in args:
            for token in element.split(" "):
                if token[0] == '#':
                    tag_args.append(token[1:])
                else:
                    notag_args.append(token)
        return tag_args, notag_args

    def add_item(self, options, args):
        """Adds an item to event list"""
        self.events.append(" ".join(args))

    @file_check
    def load_from_file(self, file_name):
        """Loads all the events from given file"""
        f = file(file_name, "rb")
        self.events = pickle.load(f)
        f.close()

    @file_check
    def save_to_file(self, file_name):
        """Saves Self.events to given file, 
        making the directories for the file if needed"""
        f = file(file_name, "wb")
        pickle.Pickler(f).dump(self.events)
        f.close()
        
    def print_items(self):
        """Prints all the items"""
        print self.events

def main(options, args):
    """Executes depending on given options"""
    has_done_something = False
    calendar = HashCal(options.file)
    if options.verbose:
        print args
        print options
        has_done_something = True
        print calendar.split_hashtags(args)
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
