#!/bin/bash
while true; do
	flask db upgrade
	if [[ "$?" == "0" ]]; then
		break
	fi
	echo Upgrade command failed, retrying in 5 secs...
	sleep 5
done
exec gunicorn -b 127.0.0.1:5000 --access-logfile - --error-logfile - app:app
