\#hashcal
========

A small command line interface for adding events to a calendar. Planning on having it connect to iCalendar eventually. 

Basically addresses the obnoxiousness of entering in events in any calendar program with the number of fields that they require by using optional hashtags.

**Dependencies**

* [docopt](https://github.com/halst/docopt) argument parser, to install: `pip install docopt`
* [vobject](https://github.com/adieu/vobject) calendar library, to install: `pip install vobject`

**Usage**

`py hashcal.py -a <phrase>`

A few examples of phrases:

`'Get dog #tomorrow #330pm'`
`'Do stats homework #apr23 #8:00'`
`'Run a marathon #octob25 #8.30pm-9am'`
`'This is event spans more than one day #23-1'`