#!/bin/bash

##
# Notify Send Telegram (github.com/MikeWent/notify-send-telegram)
# Released under the MIT license
#
# This script is just an example of use
##

# one or zero
notify_even_when_updated=0

echo "Updating apt cache..."
status=$(sudo apt update | tail -n 1 | cut -d "." -f1)
if [ "$status" == "All packages are up to date" ]
	then
	if [ $notify_even_when_updated -eq 1 ]
		then
		nst "$status"
	fi
else
	nst "Updates available" "$status"
fi
echo "Done"

