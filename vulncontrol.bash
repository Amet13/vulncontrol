#!/bin/bash

FEEDLINK="https://www.cvedetails.com/json-feed.php"
#echo "$FEEDLINK"

SOURCE="productlist.txt"
DATE=$(date +%Y-%m-%d)


while read LINK
do
	ID=$(echo "$LINK" | grep -v "#" | grep -v "^$" | cut -f5 -d"/")
	#echo "$ID"
	if [[ "$ID" != "" ]]; then
		#echo "$ID"
		#echo "$DATE"
		#curl "$FEEDLINK"
		curl "$FEEDLINK?product_id=$ID" --silent | grep "$DATE" >> file1.txt
	fi

done < "$SOURCE"
#показать уязвимости за текущий месяц

exit 0
#curl "https://www.cvedetails.com/json-feed.php?&key1=value1&key2=value2..."