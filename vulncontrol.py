#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import exit
from datetime import datetime
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads
import argparse

__author__ = 'Amet13'

# Date format: 2017-01-31
today = datetime.now().strftime('%Y-%m-%d')
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument('-t', default='', dest='TOKEN')
parser.add_argument('-i', default='', dest='ID')
namespace = parser.parse_args()

token = namespace.TOKEN
telegramid = namespace.ID

turl = 'https://api.telegram.org/bot'
tfull = '{0}{1}/sendMessage'.format(turl, token)

# Array for product IDs
ids = []
# Array for results
cves = []
# Array for Telegram results
tcves = []
# Maximum rows for one product
numrows = 10

feedlink = 'https://www.cvedetails.com/json-feed.php'
source = open('products.txt', 'r')

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
        link = '{0}?product_id={1}&year={2}&month={3}' \
            .format(feedlink, x, year, month)

        # Going to URL and get JSON
        getjson = urlopen(link)
        jsonr = getjson.read()
        for y in range(0, numrows):
            try:
                jp = loads(jsonr.decode('utf-8'))[y]
                if jp['publish_date'] == today:
                    result = '{0} {1} {2}' \
                        .format(jp['cve_id'], jp['cvss_score'], jp['url'])
                    tresult = 'CVSS: {0} URL: {1}' \
                        .format(jp['cvss_score'], jp['url'])
                    # Keep results in arrays
                    cves.append(result)
                    tcves.append(tresult)
            except (IndexError):
                break
except (ValueError, KeyError, TypeError):
    print('JSON format error')

# Getting data for Telegram
fortcves = today + ' report:\n' + '\n'.join(tcves)
tparams = urlencode({'chat_id': telegramid, 'text': fortcves}).encode('utf-8')

if len(cves) == 0:
    print('There is no available vulnerabilities today')
    exit(0)
else:
    print('\n'.join(cves))
    if token == '' or telegramid == '':
        print('Telegram alert was not sent')
        exit(1)
    else:
        try:
            urlopen(tfull, tparams)
            print('Telegram alert was sent')
            exit(2)
        except (HTTPError):
            print('Telegram alert was not sent, check your token and ID')
            exit(3)
