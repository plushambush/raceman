#!/bin/bash
GIT_COMMIT=$(git rev-parse --short HEAD)
MYEXTIP=$1
docker create  \
	--publish=5060:5060/udp \
	--publish 10000-10040:10000-10040/udp \
	--add-host=myextip:$MYEXTIP \
	--volume /var/log/raceman.log:/var/log/raceman.log \
	--name raceman \
	raceman:$GIT_COMMIT
