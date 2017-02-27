FROM raceman-base

COPY . /opt/raceman/
COPY asterisk/etc /etc/asterisk/
COPY asterisk/apps /usr/src/apps
RUN make -C /usr/src/apps/ install

VOLUME ["/var/log/raceman","/var/spool/asterisk/monitor"]
ENV PYTHONPATH=/opt/raceman
ENTRYPOINT ["asterisk"]
CMD	["-vv"]