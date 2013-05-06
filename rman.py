#!/usr/bin/python
# -*- coding: utf-8 -*-

# 50.56.75.58:50006 - arena
# 50.56.75.58:50002 - forza

from circuits.io.file import File,Read
from circuits.io.events import Write
from circuits.net.protocols.line import LP,Line
from circuits.net.sockets import TCPClient,Connect
from circuits import Component,handler,Debugger
from circuits.app import Logger
from circuits.core.pollers import Poll,EPoll,KQueue,Select
import sys
from raceman.lib.rmstream import RMStream,RMStreamEvent
from raceman.lib.rmdecoder import RMDecoder,RMEventHeartBeat,RMEventUnknown
from raceman.lib.rmanalyzer import RMAnalyzer,RMAnalyzerTarget
from raceman.lib.rmteller import RMTeller
from raceman.lib.rmagimanager import RMAGIManager,RMAGIHandler
from raceman.lib.rmagi import AGI,AGI2,AGIResult,AGIReady,AGICommand
from raceman.lib.eventqueue import EQHandlerEngaged,EQHandlerAvailable,EQHandlerBusy,EQHaveEvent,EQEnqueueEvent
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
		self._agiarg=agiarg
		try:
			_track=agiarg['agi_arg_1']
			_class=agiarg['agi_arg_2']
			_kart=agiarg['agi_arg_3']
			track=config[_track]['name']
			kart=config[_track]['park'][_class][_kart]['match']
			kartname=config[_track]['park'][_class][_kart]['name']
			self.fireEvent(RMAnalyzerTarget(track,kart,kartname))
			self.fireEvent(Connect(config[_track]['streamip'],config[_track]['streamport'],channels="rminput"))
		except AttributeError:
			pass



(Manager()+
Debugger(logger=Logger(type='file',filename="/var/log/asterisk/demo.log",level="DEBUG",name='rman'),IgnoreEvents=(Read,Line,RMEventHeartBeat,RMEventUnknown,AGIResult,RMStreamEvent,AGIReady,EQHaveEvent,EQHandlerEngaged,EQHandlerAvailable,EQHandlerBusy,EQEnqueueEvent,AGICommand))+
TCPClient(channel='rminput')+
LP(channel='rminput')+
RMStream(channel='rminput')+
RMDecoder()+
RMAnalyzer()+
RMTeller()+
RMAGIManager()+
RMAGIHandler()+
AGI2()
).run()
