#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Amet13'

import sys
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen
from json import loads, dumps

# Date format: 2017-01-31
today = datetime.now().strftime('%Y-%m-%d')
#today = '2017-02-24' # I'm using it for tests
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')

ids = [] # Array for product IDs
cves = [] # Array for results

numrows = 10 # Maximum rows for one product
feedlink = 'https://www.cvedetails.com/json-feed.php'
source = open('productlist.txt', 'r')

# Getting product IDs from file
for line in source:
	if not line.startswith('#') and line.strip():
		parsed = urlparse(line)
		path = parsed[2]
		pathlist = path.split("/")
		ids.append(pathlist[2])

source.close()

# Get JSON for out products today
try:
	for x in ids:
		# Link example:
		# https://www.cvedetails.com/json-feed.php?product_id=47&year=2017&month=02
		link = feedlink + '?product_id=' + x + '&year=' + year + '&month=' + month
		# Going to URL and get JSON
		getjson = urlopen(link)
		jsonr = getjson.read()
		for y in range(0, numrows):
			try:
				jsonp = loads(jsonr.decode('utf-8'))[y]
				if jsonp['publish_date'] == today:
					result = jsonp['cve_id'] + " " + jsonp['cvss_score'] + " " + jsonp['url']
					cves.append(result)
			except IndexError:
				break
except (ValueError, KeyError, TypeError):
	print ('JSON format error')

if len(cves) == 0:
	print ('There is no available vulnerabilities today')
	sys.exit(0)
else:
	print (*cves)
	sys.exit(1)

# Output:
# $ ./vulncontrol.py
# ['CVE-2017-5669 4.6 http://www.cvedetails.com/cve/CVE-2017-5669/']