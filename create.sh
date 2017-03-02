#!/bin/bash
docker container create  \
	--publish=10.0.2.5:5060:5060/udp \
	--publish 10.0.2.5:10000-10040:10000-10040/udp \
	--add-host=myextip:$(dig +short myip) \
	--volume /var/log/raceman.log:/var/log/raceman.log \
	--name raceman \
	raceman
