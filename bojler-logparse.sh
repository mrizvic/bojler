#!/bin/sh
/usr/bin/bzgrep "bojler.py: event" /var/log/all.log.0.bz2
echo -n "SUM(delta) = "
/usr/bin/bzgrep "bojler.py: event" /var/log/all.log.0.bz2 | grep delta | cut -d '=' -f4 | awk '{ sum += $1; c++ } END { print sum/60 " min"} '
