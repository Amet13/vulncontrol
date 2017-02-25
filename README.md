vulncontrol
===========
Python script for monitoring www.cvedetails.com vulnerabilities database.

Usage
-----

Add software what you need to `productlist.txt`.

You can search software here: https://www.cvedetails.com/product-search.php

Then you can run script:
```
$ ./vulncontrol.py
['CVE-2017-5669 4.6 http://www.cvedetails.com/cve/CVE-2017-5669/']
```

Script collects list of software from file and find all vulnerabilities for current date (today).

You can customize `result` with more values.
Available keys:
* `cve_id`
* `cvss_score`
* `cwe_id`
* `exploit_count`
* `publish_date`
* `summary`
* `update_date`
* `url`

For example:
```
result = jsonp['cve_id'] + " " + jsonp['cvss_score'] + " " + jsonp['url'] + " " + jsonp['summary'] + " " + jsonp['exploit_count']

$ ./vulncontrol.py
['CVE-2017-5669 4.6 http://www.cvedetails.com/cve/CVE-2017-5669/ The do_shmat function in ipc/shm.c in the Linux kernel through 4.9.12 does not restrict the address calculated by a certain rounding operation, which allows local users to map page zero, and consequently bypass a protection mechanism that exists for the mmap system call, by making crafted shmget and shmat system calls in a privileged context. 0']
```

Example of JSON-output:
```
{
	"cve_id": "CVE-2017-5551",
	"cvss_score": "3.6",
	"cwe_id": "264",
    "exploit_count": "0",
    "publish_date": "2017-02-06",
    "summary": "The simple_set_acl function in fs/posix_acl.c in the Linux kernel before 4.9.6 preserves the setgid bit during a setxattr call involving a tmpfs filesystem, which allows local users to gain group privileges by leveraging the existence of a setgid program with restrictions on execute permissions.  NOTE: this vulnerability exists because of an incomplete fix for CVE-2016-7097.",
    "update_date": "2017-02-09",
    "url": "http://www.cvedetails.com/cve/CVE-2017-5551/"
}
```

www.cvedetails.com API
----------------------
```
curl "https://www.cvedetails.com/json-feed.php?&key1=value1&key2=value2..."
```

Custom parameters:

| Key          | Value | Description                                                    |
| ------------ | ----- | -------------------------------------------------------------- |
| year         | 2017  | [Year](http://www.cvedetails.com/browse-by-date.php)           |
| month        | 1-12  | [Month](http://www.cvedetails.com/browse-by-date.php)          |
| vendor_id    | 33    | [Vendor ID](http://www.cvedetails.com/vendor.php)              |
| product_id   | 47    | [Product ID](http://www.cvedetails.com/product-list.php)       |
| orderby      | 1-3   | Sort type (1 - Publish Date, 2 - Last Update Date, 3 - CVE ID) |
| cvssscoremin | 0-10  | Min CVSS                                                       |
| cvssscoremax | 0-10  | Max CVSS                                                       |
| numrows      | 0-30  | Number of rows                                                 |

Boolean parameters (0 by default, 1 - yes):

| Key       | Value | Description                |
| --------- | ----- | -------------------------- |
| hasexp    | 0     | Has exploits               |
| opec      | 0     | Code execution             |
| opov      | 0     | Overflows                  |
| opcsrf    | 0     | Cross Site Request Forgery |
| opfileinc | 0     | File inclusion             |
| opgpriv   | 0     | Gain privilege             |
| opsqli    | 0     | Sql injection              |
| opxss     | 0     | Cross site scripting       |
| opdirt    | 0     | Directory traversal        |
| opmemc    | 0     | Memory corruption          |
| ophttprs  | 0     | Http response splitting    |
| opbyp     | 0     | Bypass something           |
| opginf    | 0     | Gain information           |
| opdos     | 0     | Denial of service          |

TODO
----
* Integrate with monitoring (Zabbix, Nagios/Icinga2 or cron running with email alert)
* Log file for vulnerabilities
* Mark CVE as safety
* Set parameter in script
* Interactive mode
* Telegram alert (if monitoring does not using)