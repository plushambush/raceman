#!/usr/bin/python
# -*- coding: utf-8 -*-

# 50.56.75.58:50006 - arena
# 50.56.75.58:50002 - forza


from circuits.io import File
from circuits.io.events import Write
from circuits.net.protocols import LP
from circuits.net.sockets import TCPClient,Connect
from circuits import Component,handler,Debugger

import sys

from raceman.lib.rmstream import RMStream
from raceman.lib.rmdecoder import RMDecoder
from raceman.lib.rmanalyzer import RMAnalyzer,RMAnalyzerTarget
from raceman.lib.rmteller import RMTeller
from raceman.lib.rmagimanager import RMAGIManager,RMAGIHandler
from raceman.lib.rmagi import AGI
from signal import SIGHUP
from exceptions import AttributeError
from raceman.lib.config import config

class Manager(Component):
    """MAIN manager"""
    @handler("agihangup")
    def _agihangup(self):
        self.stop()

    @handler("signal")
    def _signal(self,sig,sigtype):
        if sig==SIGHUP:
            self.stop()

    @handler("agistartupcomplete")
    def _agistartupcomplete(self,agiarg):
#        if hasattr(agiargs,'agi_arg_2'):
        self._agiarg=agiarg
        try:
            self.fireEvent(RMAnalyzerTarget(agiarg['agi_arg_1'],config[agiarg['agi_arg_1']]['park'][agiarg['agi_arg_2']][agiarg['agi_arg_3']]))
            self.fireEvent(Connect(config[agiarg['agi_arg_1']]['streamip'],config[agiarg['agi_arg_1']]['streamport'],channels="rminput"))
        except AttributeError:
            pass

    

(Manager()+
Debugger(file="/var/log/asterisk/demo.log")+
TCPClient(channel='rminput')+
#File(filename='stream0.txt',channel='rminput')+
LP(channel='rminput')+
RMStream(channel='rminput')+
RMDecoder()+
RMAnalyzer()+
RMTeller()+
AGI()+
RMAGIManager()+
RMAGIHandler()).run()