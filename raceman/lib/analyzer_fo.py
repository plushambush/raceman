from circuits.core import Component,handler,Event,Timer
from raceman.lib.events_info import *
from raceman.lib.events_announce import *
from raceman.lib.config import *
from raceman.lib.rmcomponent import RMComponent

class RMAnalyzerAnnounceRace(Event):
	""" Timer event to announce current race state"""

class RMAnalyzerFO(RMComponent):
	def __init__(self,*args,**kwargs):
		super(RMAnalyzerFO,self).__init__(*args,**kwargs)
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
		self.fire(RMAnnounceRaceStopped(raceid), 'announce')
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
	def on_rminfo_race_nodata(self):
		self.fire(RMAnnounceRaceNoData(), 'announce')
		self.push_state('RACENODATA')
		
	@handler("RMInfoRaceDataBack", channel='infoevents')
	def on_rminfo_race_data_back(self):
		self.fire(RMAnnounceRaceDataBack(), 'announce')
		self.pop_state()


	@handler("RMAnalyzerAnnounceRace")
	def on_analyzer_announce_race(self):
		if self._state=='RACESTOPPED':
			self.fire(RMAnnounceRaceFinished(None))
		elif self._state=='RACEWAITING':
			self.fire(RMAnnounceRaceWaiting())
		elif self._state=='RACENORACE':
			self.fire(RMAnnounceRaceNoRace())
		elif self._state=='RACENODATA':
			self.fire(RMAnnounceRaceNoData())
	
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






