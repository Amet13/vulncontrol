vulncontrol
===========
Python script for monitoring www.cvedetails.com vulnerabilities database.

Usage
-----
```
$ ./vulncontrol.py
['CVE-2017-5669 4.6 http://www.cvedetails.com/cve/CVE-2017-5669/']
```

cvedetails.com API
------------------
```
curl "https://www.cvedetails.com/json-feed.php?&key1=value1&key2=value2..."

year=2017 # Year, http://www.cvedetails.com/browse-by-date.php
month=2 # Month (1 - 12), http://www.cvedetails.com/browse-by-date.php
vendor_id=33 # Vendor ID, http://www.cvedetails.com/vendor.php
product_id=47 # Product ID, http://www.cvedetails.com/product-list.php

Boolean (0 by default):
hasexp=0 # Has exploits
opec=0 # Code execution
opov=0 # Overflows
opcsrf=0 # Cross Site Request Forgery
opfileinc=0 # File inclusion
opgpriv=0 # Gain privilege
opsqli=0 # Sql injection
opxss=0 # Cross site scripting
opdirt=0 # Directory traversal
opmemc=0 # Memory corruption
ophttprs=0 # Http response splitting
opbyp=0 # Bypass something
opginf=0 # Gain information
opdos=0 # Denial of service

orderby=0 # Sort by (1 - Publish Date, 2 - Last Update Date, 3 - CVE ID)
cvssscoremin=0 # Min CVSS (0 - 10)
cvssscoremax=0 # Max CVSS (0 - 10)
numrows=30 # Number of rows (0 - 30)
```

TODO
----
* Integrate with monitoring (Zabbix, Nagios/Icinga2 or cron running with email alert)
* Log file for vulnerabilities
* Mark CVE as safety