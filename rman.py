#!/usr/bin/python -u
# -*- coding: utf-8 -*-


from circuits import Component,handler,Debugger,Event
from circuits.web.loggers import Logger
from circuits.core.pollers import Poll,EPoll,KQueue,Select
import sys
from raceman.lib.rmstream import RMStream,RMStreamEvent
from raceman.lib.rmdecoder import RMDecoder,RMEventHeartBeat,RMEventUnknown
from raceman.lib.teller_static import RMTeller_Static
from raceman.lib.eventqueue import EQHandlerEngaged,EQHandlerAvailable,EQHandlerBusy,EQHaveEvent,EQEnqueueEvent
from signal import SIGHUP
from exceptions import AttributeError
from raceman.lib.config import *
import raceman.lib.config as config
import raceman.lib.config_tracks as config_tracks
import raceman.lib.config_profiles as config_profiles
from raceman.lib.config_profiles import *
from raceman.lib.sound_pygame import *
from raceman.lib.sound_base import *
from raceman.lib.events_connector import *
from raceman.lib.analyzer_fo import *
from pdb import set_trace
from os import environ

from raceman.lib.connector_fo import RMConnectorFO

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
	def on_startup(self, prog_name, userID='default_user', trackID='forza-fo', classID=1, targetN='0', rivalN='0'):
		self.fire(RMParams('======STARTUP PARAMETERS:',sys.argv,environ.get('SDL_AUDIODRIVER','NO_DRIVER'),environ.get('SDL_DISKAUDIOFILE','NOFILE')))
		config.track = config_tracks.tracks[trackID]		
		config.profile=config_profiles.profiles[userID]
		config.target=int(targetN)
		config.rival=int(rivalN)
		_connector=config.track['connector']
		_connector().register(self)
		self.fire(RMAnnounceTrackSelected(config.track['name']),'announce')
		self.fire(RMConnectorStart())
		self.fire(RMAnnounceKartSelected(config.target),'announce')
		if config.rival:
			self.fire(RMAnnounceRivalSelected(config.rival),'announce')

	@handler("started")
	def _started(self,komponent):
		# parameters
		# - userid		
		# - trackid		
		# - kart_class_id		
		# - target kart N		
		# - rival kart N		


		self.fireEvent(RMStartup(*sys.argv))
		

(Manager()+
Debugger(IgnoreEvents=['read','_read','write','_write'],file=RMSYSTEM_LOGFILE)+
RMAnalyzerFO()+
RMTeller_Static()+
RMSound_Pygame()
).run()
