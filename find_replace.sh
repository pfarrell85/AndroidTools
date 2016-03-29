#!/bin/sh

if [ "$#" -lt 1 ]; then
	echo "Error"
	exit 1
else 
	grep -rl $1 * -R | xargs sed -i 's/'$1'/'$2'/g'
fi