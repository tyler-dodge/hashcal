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
import dateparser
import tokenize
import pickle
import os
import vobject

def file_check(fn):
	def wrap(self, file_name, *args):
		# create directory if it doesn't exist
		directory = file_name[:file_name.rfind("/")]
		if not os.path.exists(directory):
			os.makedirs(directory) 
		# create file if it doesn't exist
		if not os.path.exists(file_name):
			file(file_name, "w").close() 
		fn(self, file_name, *args)
	return wrap

def write_ics(filename, start, end, description):
	ical = vobject.iCalendar()
	ical.add('vevent')
	event = ical.vevent
	event.add('dtstart').value = start
	event.add('dtend').value = end
	event.add('summary').value = description
	event.add('prodid').value = 'hashcal'

	file = open(filename, 'w')
	file.write( ical.serialize() )
	file.close()
def write_appleScript(name,start, end, description):
    
    script = "".join((
            'tell application "iCal"\n',
            'set theCalendarNames to title of every calendar\n',
            'set cal to item 1 of theCalendarNames\n'
            'end tell\n',
            'tell application "iCal"\n', 
            'tell calendar cal\n',
            'make new event at end with properties\n',
            '{description:"%s",\n' % description,
            'summary:"%s",\n' % description,
            'start date:"%s",\n' % start,
            'end date:"%s",\n' % end,
            'event:true}\n',
            'end tell\n',
            'end tell\n'))
    print script
    os.system("osascript <<< '%s'" % script)

class HashCal(object):
	def __init__(self, source_file=None):
		"""Create HashCal. If file is given, load events from it"""

		if source_file is not None:
			self.load_from_file(source_file)
		else:
			self.events = []

	def split_hashtags(self, args):
		"""Given a set of args, will return:
			An array of all the hashtagged args with the hashtags stripped, 
			and a word with the description"""

		tags = []
		description = ""
		for element in args:
			for token in element.split(" "):
				if token[0] == '#':
					tags.append(token[1:])
				else:
					if len(description)>0: description += " "
					description += token
		return tags, description

	def add_item(self, options, tags, description):
		"""Adds an item to event list"""
		print tags, description
		start,end = dateparser.parse_tags(tags)
		print start,end
		self.events.append( { 'start': start, 'end': end, 'text': description })
		write_ics('test.ics', start, end, description)
		write_appleScript("",start,end,description)

	@file_check
	def load_from_file(self, file_name):
		"""Loads all the events from given file"""

		f = file(file_name, "rb")
		# Make sure file isn't empty when loading the
		# pickle, or it will give EOFERROR
		if os.path.getsize(file_name) > 0:
			self.events = pickle.load(f)
		else:
			self.events = []
		f.close()

	@file_check
	def save_to_file(self, file_name):
		"""Saves Self.events to given file, 
		making the directories for the file if needed"""

		f = file(file_name, "wb")
		pickle.dump(self.events, f)
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

	if options.add:
		tags, description = calendar.split_hashtags(args)
		calendar.add_item(options, tags, description)
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
