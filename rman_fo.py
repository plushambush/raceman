#!/usr/bin/python -u
# -*- coding: utf-8 -*-


# 50.56.75.58:50006 - arena
# 50.56.75.58:50002 - forza

from circuits import Component,handler,Debugger,Event
from circuits.web.loggers import Logger
from circuits.core.pollers import Poll,EPoll,KQueue,Select
import sys
from raceman.lib.rmstream import RMStream,RMStreamEvent
from raceman.lib.rmdecoder import RMDecoder,RMEventHeartBeat,RMEventUnknown
from raceman.lib.rmanalyzer import RMAnalyzer,RMAnalyzerTarget
from raceman.lib.rmteller_sapi import RMTeller_SAPI
from raceman.lib.eventqueue import EQHandlerEngaged,EQHandlerAvailable,EQHandlerBusy,EQHaveEvent,EQEnqueueEvent
from signal import SIGHUP
from exceptions import AttributeError
from raceman.lib.config import config
from raceman.lib.rmsound_pygame import *
from raceman.lib.rmsound_base import *
from raceman.lib.rmtts_sapi import *
from raceman.lib.rmconnectorevents import *
from pdb import set_trace
from os import environ

from raceman.lib.rmconnectorfo import RMConnectorFO

class RMStartup(Event):
	pass


class RMParams(Event):
	pass

class Manager(Component):
	"""MAIN manager"""

	@handler("RMParams")
	def _on_rm_params(self,*args,**kwargs):
		pass

	@handler("signal")
	def _signal(self,sig,sigtype):
		if sig==SIGHUP:
			self.stop()

	@handler("RMStartup")
	def on_startup(self,trackID,classID,kartID):
		self.fire(RMParams('======STARTUP PARAMETERS:',sys.argv,environ.get('SDL_AUDIODRIVER','NO_DRIVER'),environ.get('SDL_DISKAUDIOFILE','NOFILE')))
		self.fire(RMConnectorConfigure(config,classID,kartID))
		self.fire(RMConnectorStart())

	@handler("started")
	def _started(self,komponent):
		self.fireEvent(RMStartup(sys.argv[1],sys.argv[2],sys.argv[3]))
		

(Manager()+
Debugger(IgnoreEvents=['read','_read','write','_write'])+
RMConnectorFO()+
RMTeller_SAPI()+
RMTTS_SAPI()+
RMSound_Pygame()
).run()
