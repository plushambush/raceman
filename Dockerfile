FROM debian:jessie
RUN apt-get update && apt-get install -y \
	python2.7-minimal \
	asterisk \
	asterisk-dev \
	python-pygame \
	python-pip && \
	pip install circuits

COPY . /opt/raceman/
COPY asterisk/etc /etc/asterisk/
COPY asterisk/apps /usr/src/apps
RUN make -C /usr/src/apps/ install && rm -rf /usr/src/apps && rm -rf /opt/raceman/asterisk

VOLUME ["/var/log/","/var/spool/asterisk/monitor"]
ENV PYTHONPATH=/opt/raceman
ENTRYPOINT ["asterisk"]
CMD	["-vv"]
EXPOSE 5060/UDP 10000-10040/UDP
