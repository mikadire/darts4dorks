#!/bin/bash
while true; do
	flask db upgrade
	if [[ "$?" == "0" ]]; then
		break
	fi
	echo Upgrade command failed, retrying in 5 secs...
	sleep 5
done
exec gunicorn -b :5000 -w 3 --access-logfile /dev/null --error-logfile - app:app
