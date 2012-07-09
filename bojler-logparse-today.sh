#!/bin/sh
/usr/bin/grep "bojler.py: event" /var/log/all.log
echo -n "SUM(delta) = "
/usr/bin/grep "bojler.py: event" /var/log/all.log | grep delta | cut -d '=' -f4 | awk '{ sum += $1; c++ } END { print sum/60 " min"} '
