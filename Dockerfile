FROM raceman-base

COPY . /opt/raceman/
COPY asterisk/etc /etc/asterisk/
COPY asterisk/apps /usr/src/apps
RUN make -C /usr/src/apps/ install

VOLUME ["/var/log/raceman.log","/var/spool/asterisk/monitor"]
ENV PYTHONPATH=/opt/raceman
ENTRYPOINT ["asterisk"]
CMD	["-vv"]
EXPOSE 5060/UDP 10000-20000/UDP
