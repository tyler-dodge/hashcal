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
	if options.verbose:
		print args
		print options
	if options.add:
		addItem(options, args)
	if options.show:
		printItems()


def addItem(options, args):
	if not os.path.exists(options.file):
		os.makedirs(options.file[:options.file.rfind("/")])
	f = file(options.file, "wb")
	pickle.Pickler(f).dump(args)
	f.close()


def printItems():
	f = file(options.file, "rb")
	print pickle.load(f)
	f.close()

if __name__ == '__main__':
	options, args = docopt(__doc__)
	options.file = os.path.expanduser(options.file)
	main(options, args)
