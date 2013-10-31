#!/usr/bin/python -u
# -*- coding: utf-8 -*-


# 50.56.75.58:50006 - arena
# 50.56.75.58:50002 - forza

from circuits.io.file import File,Read
from circuits.io.events import Write
from circuits.net.protocols.line import LP,Line
from circuits.net.sockets import TCPClient,Connect
from circuits import Component,handler,Debugger,Event
from circuits.app import Logger
from circuits.core.pollers import Poll,EPoll,KQueue,Select
import sys
from raceman.lib.rmstream import RMStream,RMStreamEvent
from raceman.lib.rmdecoder import RMDecoder,RMEventHeartBeat,RMEventUnknown
from raceman.lib.rmanalyzer import RMAnalyzer,RMAnalyzerTarget
from raceman.lib.rmteller import RMTeller
from raceman.lib.rmagisound import RMAGISound
from raceman.lib.rmagi import AGI,AGIResult,AGIReady,AGICommand
from raceman.lib.eventqueue import EQHandlerEngaged,EQHandlerAvailable,EQHandlerBusy,EQHaveEvent,EQEnqueueEvent
from signal import SIGHUP
from exceptions import AttributeError
from raceman.lib.config import config
from raceman.lib.rmsound_pygame import *
from raceman.lib.rmsound_base import *
from raceman.lib.rmtts_festival import *
from pdb import set_trace
from os import environ

class RMStartup(Event):
	pass


class RMParams(Event):
	pass

class Manager(Component):
	"""MAIN manager"""

	@handler("rm_params")
	def _on_rm_params(self,*args,**kwargs):
		pass

	@handler("signal")
	def _signal(self,sig,sigtype):
		if sig==SIGHUP:
			self.stop()

	@handler("rmstartup")
	def _agistartupcomplete(self,trackID,classID,kartID):
		self.fireEvent(RMParams('======STARTUP PARAMETERS:',sys.argv,environ.get('SDL_AUDIODRIVER','NO_DRIVER'),environ.get('SDL_DISKAUDIOFILE','NOFILE')))
		self.fireEvent(RMAnalyzerTarget(trackID,classID,kartID))
		self.fireEvent(Connect(config[trackID]['streamip'],config[trackID]['streamport'],channels="rminput"))

	@handler("started")
	def _started(self,komponent):
		self.fireEvent(RMStartup(sys.argv[1],sys.argv[2],sys.argv[3]))


(Manager()+
Debugger(logger=Logger(type='file',filename="/home/ricochet/Projects/raceman/raceman.log",level="DEBUG",name='rman'),IgnoreEvents=['rmsound_driver_play_stream_sync','rmsound_play_stream','rmsound_driver_play_stream_sync_complete'])+
TCPClient(channel='rminput')+
LP(channel='rminput')+
RMStream(channel='rminput')+
RMDecoder(channel='rminput')+
RMAnalyzer()+
RMTeller()+
RMTTS_Festival()+
RMSound_Pygame()
).run()
