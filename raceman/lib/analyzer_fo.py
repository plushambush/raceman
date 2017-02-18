from circuits.core import Component,handler,Event,Timer
from raceman.lib.events_info import *
from raceman.lib.events_announce import *
from raceman.lib.config import *
import raceman.lib.config as config
from raceman.lib.rmcomponent import RMComponent
from raceman.lib.racingtime import RacingTime
import pdb

class RMAnalyzerAnnounceRace(Event):
	""" Timer event to announce current race state"""

class RMAnalyzerFO(RMComponent):
	def __init__(self,*args,**kwargs):
		super(RMAnalyzerFO,self).__init__(*args,**kwargs)
		self.bestlap=False
		self._racetimer=Timer(FO_ANNOUNCE_PERIOD,RMAnalyzerAnnounceRace(),persist=True).register(self)


	@handler("RMConnectorConnected", channel='infoevents')
	def on_rmconnector_connected(self):
		self.fire(RMAnnounceConnected())
		
	@handler("RMInfoRaceStarted", channel='infoevents')
	def on_rminfo_race_started(self,raceid):
		self.fire(RMAnnounceRaceStarted(raceid), 'announce')
		self.change_state('RACEGOING')
		
	
	@handler ("RMInfoRaceStopped", channel='infoevents')
	def on_rminfo_race_stopped(self,raceid):
		self.fire(RMAnnounceRaceStopped(), 'announce')
		self.change_state('RACESTOPPED')


	@handler("RMInfoRaceWaiting", channel='infoevents')
	def on_rminfo_race_waiting(self):
		self.fire(RMAnnounceRaceWaiting(), 'announce')
		self.change_state('RACEWAITING')
		
		
	@handler("RMInfoRaceNoRace", channel='infoevents')
	def on_rminfo_race_norace(self):
		self.fire(RMAnnounceRaceNoRace(), 'announce')
		self.change_state('RACENORACE')

	@handler("RMInfoRaceNoData", channel='infoevents')
	def on_rminfo_race_nodata(self,raceid):
		self.fire(RMAnnounceRaceNoData(), 'announce')
		self.push_state('RACENODATA')
		
	@handler("RMInfoRaceDataBack", channel='infoevents')
	def on_rminfo_race_data_back(self):
		self.fire(RMAnnounceRaceDataBack(), 'announce')
		self.pop_state()


	@handler("RMAnalyzerAnnounceRace")
	def on_analyzer_announce_race(self):
		if self._state=='RACESTOPPED':
			self.fire(RMAnnounceRaceStopped(),'announce')
		elif self._state=='RACEWAITING':
			self.fire(RMAnnounceRaceWaiting(),'announce')
		elif self._state=='RACENORACE':
			self.fire(RMAnnounceRaceNoRace(),'announce')
		elif self._state=='RACENODATA':
			self.fire(RMAnnounceRaceNoData(),'announce')
	
	
	
	@handler("RMInfoKartLap", channel='infoevents')
	def on_rival_lap(self,num,is_target,is_rival,lap,blap,alap,bblap,time):
		if is_rival:
			self.fire(RMAnnounceRivalLap(num,lap,time),'announce')


	@handler("RMInfoKartLap", channel='infoevents')
	def on_target_lap(self,num,is_target,is_rival,lap,blap,alap,bblap,time):
		if is_target:
			if lap<bblap:
				self.fire(RMAnnounceKartBestLap(),'announce')
				self.bestlap=True
			elif (lap-bblap)<RacingTime.fromint(config.profile['BETTER_DELTA']):
				self.fire(RMAnnounceKartLapBetter(alap),'announce')
			elif (lap>alap):
				self.fire(RMAnnounceKartLapWorse(alap))
			self.fire(RMAnnounceTargetLap(num,lap,time),'announce')
			
	@handler("RMInfoKartLap", channel='infoevents')
	def on_lost_bestlap(self,num,is_target,is_rival,lap,blap,alap,bblap,time):
		if lap<bblap and not is_target and self.bestlap:
			self.bestlap=False
			self.fire(RMAnnounceKartLostBestLap(num,lap))
			
	
class RMInfoKartLap(Event):
	"""Target kart finished lap
	kart num (integer)
	is_target (boolean)
	is_rival (boolean)
	laptime (RacingTime)
	sessiontime (RacingTime)
	best time (RacingTime)
	average time (RacingTime)
	"""

class RMInfoKartBestLap(Event):
	"""Target kart set best lap"""

class RMInfoKartLostBestLap(Event):
	"""Kart lost best lap"""
    
class RMInfoKartLapBetter(Event):
	"""Kart lap time is better then average
	Params:
		- Avgtime - average time
	"""

class RMInfoKartLapWorse(Event):
	"""Kart lap time is worse then average"""


class RMInfoTrackSelected(Event):
	"""Track selected as target"""






