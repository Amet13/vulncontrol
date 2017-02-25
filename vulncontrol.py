#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Amet13'

from sys import exit, argv
from datetime import datetime
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen
from json import loads, dumps

# Date format: 2017-01-31
today = datetime.now().strftime('%Y-%m-%d')
#today = '2017-02-24' # I'm using it for tests
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')

# Telegram things
try:
	token = str(argv[1])
	telegramid = str(argv[2])
except (IndexError):
	print ('You are not using token and ID for Telegram')
	token = ''
	telegramid = ''

turl = 'https://api.telegram.org/bot'
tfull = turl + token + '/sendMessage'

ids = [] # Array for product IDs
cves = [] # Array for results
tcves = [] # Array for Telegram results

numrows = 10 # Maximum rows for one product
feedlink = 'https://www.cvedetails.com/json-feed.php'
source = open('productlist.txt', 'r')

# Getting product IDs from file
for line in source:
	if not line.startswith('#') and line.strip():
		parsed = urlparse(line)
		path = parsed[2]
		pathlist = path.split('/')
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
					result = jsonp['cve_id'] + ' ' + jsonp['cvss_score'] + ' ' + jsonp['url']
					tresult = 'CVSS:' + jsonp['cvss_score'] + ' URL: ' + jsonp['url']
					cves.append(result)
					tcves.append(tresult)
			except (IndexError):
				break
except (ValueError, KeyError, TypeError):
	print ('JSON format error')

# Getting data for Telegram
tparams = urlencode({'chat_id': telegramid, 'text': tcves}).encode('utf-8')

if len(cves) == 0:
	print ('There is no available vulnerabilities today')
	exit(0)
else:
	print (*cves)
	if token == '' or telegramid == '':
		print ('Telegram alert does not sent')
		exit(1)
	else:
		urlopen(tfull, tparams)
		print ('Telegram alert was sent')
		exit(2)
