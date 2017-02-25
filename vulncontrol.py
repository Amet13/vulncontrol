#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Amet13'
#import os
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen
from json import loads, dumps
#import re
#import json
#import urllib2

feedlink = 'https://www.cvedetails.com/json-feed.php'
#today = datetime.now().strftime('%Y-%m-%d')# Date format 2017-01-31
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')
source = open('productlist.txt', 'r')
ids = [] # Array for Product IDs

# Getting Product IDs from file
for line in source:
	if not line.startswith('#') and line.strip():
		parsed = urlparse(line)
		path = parsed[2]
		pathlist = path.split("/")
		ids.append(pathlist[2])

source.close()

# Get JSON for out products by current year and month
try:
	for x in ids:
		#x = '47'
		# Link example
		# https://www.cvedetails.com/json-feed.php?product_id=47&year=2017&month=02
		link = feedlink + '?product_id=' + x + '&year=' + year + '&month=' + month
		# Going to URL and get JSON
		getjson = urlopen(link)
		# Do JSON pretty
		jsonout = getjson.read().decode('utf-8')
		jsonparsed = loads(jsonout)
		print (dumps(jsonparsed, sort_keys=True, indent=4))

except (ValueError, KeyError, TypeError):
    print ('JSON format error')

#print (today)
