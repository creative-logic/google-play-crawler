import calendar
import datetime

import dateparser

switch = {
	"in the last week": "the last week"
}

def utctimestamp(dt):
    return calendar.timegm(dt.utctimetuple())


def nowts():
    return utctimestamp(datetime.datetime.now())


def parse_date_ts(date_string):
	date_string = switch.get(date_string) if switch.get(date_string) else date_string

	dt = dateparser.parse(date_string)
	if dt:
		return utctimestamp(dt)