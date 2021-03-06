#!/bin/bash

##
# Notify Send Telegram (github.com/MikeWent/notify-send-telegram)
# Released under the MIT license
#
# This script is just an example of use
##

while true; do
	sudo tail -n 0 -f /var/log/syslog | while read line; do
		echo $line
		./notify-send-telegram.py -r YOUR_USER_ID -t YOUR_BOT_TOKEN 'Syslog message' "$line"
		sleep 0.25
	done
done
