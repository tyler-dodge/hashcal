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
import datetime
import re

#TODO make this a class so it's prettier
def parse_datetime(tags):

	now = datetime.datetime.today()
	def parse_day(tag):
		weekdays = [
			'monday', 'tuesday', 'wedesnday', 'thursday', 
			'friday', 'saturday', 'sunday'
		]
		months = [
			'january', 'february', 'march', 'april',
			'may', 'june', 'july', 'august', 'september', 
			'october', 'novemember', 'december'
		]

		if 'today'.find(tag)==0:
			return now

		if 'tomorrow'.find(tag)==0:
			return now + datetime.timedelta(1)

		# See if it's a weekday
		for day_num,day in enumerate(weekdays):
			if day.find(tag)==0:
				delta_day = 1+day_num-now.isoweekday() % 7
				return now + datetime.timedelta(delta_day)

		# Then see if it's a month and day like apr23
		mo = filter(lambda c: c.isalpha(), tag);
		if len(mo)>0:
			day = filter(lambda c: c.isdigit(), tag)
			if len(day)>0:
				day = int(day)
				for month_num,month in enumerate(months):
					if month.find(mo)==0:
						print mo, month
						year = now.year
						# if it's next year
						if 1+month_num < now.month:
							year += 1
						return datetime.datetime(year, 1+month_num, day)

		# else it's not a day
		return None

	def parse_time(tag):
		# determine if it's actually a parseable time with regex
		is_time_regex = [
			'\d{1,4}', # eg 1pm or 830pm or 1430
			'\d{1,2}[\.:]\d{2}', # eg 8:30pm or 14.30
		]
		# Return None if it's not a day
		is_date = False
		for regexp in is_time_regex:
			if re.match(regexp, tag) != None:
				is_date = True
		if not is_date:
			return None

		# If it's a day, go ahead
		duration = tag.split('-')
		times = []
		for expr in duration:
			pm = 'pm' in expr.lower()
			time = int(filter(lambda c: c.isdigit(), expr))
			if time<=24: #if it's just eg "#1pm" or "#24"
				if pm: time += 12
				times.append(datetime.time(timegit,0))
			else:
				hour = time / 100
				if pm: hour += 12
				minute = time % 100
				times.append(datetime.time(hour,minute))
		if len(times)==1:
			start = times[0]
			end = datetime.time((1+start.hour)%24, start.minute)
			times.append(end)
		return times

	date = None
	times = None
	for tag in tags:
		tag = tag.lower()
		# tag is either a date or a time, can't be both
		if date == None:
			date = parse_day(tag)
		if times == None:
			times = parse_time(tag)

	if date == None:
		date = now
		print "Defaulting to today, could not find date"
	if times == None:
		times = [ datetime.time(0), datetime.time(0) ]
		print "Defaulting to 0 minute event, could not find time"

	start = datetime.datetime(date.year, date.month, date.day, times[0].hour, times[0].minute, 0)
	end = datetime.datetime(date.year, date.month, date.day, times[1].hour, times[1].minute, 0)
	if times[1] < times[0]:
		end += datetime.timedelta(1) # add one day if the time goes into next day

	return start, end

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
		start,end = parse_datetime(tags)
		print start,end
		self.events.append( { 'start': start, 'end': end, 'text': description })
		

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
