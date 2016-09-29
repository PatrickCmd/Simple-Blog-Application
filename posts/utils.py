import datetime
from math import *
import re

from django.utils.html import strip_tags


def count_words(html_string):
	""" Return count of words from an html document """	
	# html_string = """</h1>This is an html heading one tag </h1>"""
	word_string = strip_tags(html_string)
	matching_words = re.findall(r'\w+', word_string)     # returns a list of words from word_string
	count = len(matching_words)
	return count


def get_read_time(html_string):
	""" Return read time in seconds """

	count = count_words(html_string)
	read_time_min = ceil((count / 200.0))     # assuming read time 200 words per min
	# read_time_sec = read_time_min * 60
	# read_time = str(datetime.timedelta(seconds=read_time_sec))
	read_time = str(datetime.timedelta(minutes=read_time_min))

	return read_time