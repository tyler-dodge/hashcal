"""Usage: hashcal.py [options] arguments

Options:
  -h --help       show this help message and exit
  -v --verbose    print status messages
  -q --quiet      print only success or failure
  --version       print the current version
  -a --add        add an item to the list
  -s --show       show all items in the list
"""
from docopt import docopt
import pickle

def main(options, args):
	print args
	print options
	if options.add:
		addItem(args)
	if options.show:
		printItems()


def addItem(args):
	f = file("test.dat", "wb")
	pickle.Pickler(f).dump({ 'yourMom': args[0] })
	f.close()


def printItems():
	f = file("test.dat", "rb")
	print pickle.load(f)
	f.close()

if __name__ == '__main__':
	options, args = docopt(__doc__)
	main(options, args)