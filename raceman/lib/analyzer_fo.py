from circuits.core import Compoent,handler,Event,Timer
from raceman.lib.events_info import *
from raceman.lib.events_announce import *

class RMAnalyzer(Component)
	def __init__(self,*args,**kwargs):
		super(RMAnalyzer,self).__init__(*args,**kwargs)
		self._racetimer=None
		
	@handler("RMInfoRaceStarted", channel='infoevents')
	def on_rminfo_race_started(self,raceid):
		self.fire(RMAnnounceRaceStarted(raceid), 'announce')
		
	
	@handler ("RMInfoRaceStopped", channel='infoevents')
	def on_rminfo_race_stopped(self,raceid):
		self.fire(RMAnnounceRaceStopped(raceid), 'announce')


	@handler("RMInfoRaceWaiting", channel='infoevents')
	def on_rminfo_race_waiting(self,raceid):
		self.fire(RMAnnounceRaceWaiting(raceid), 'announce')
		
		
	@handler("RMInfoRaceNoRace", channel='infoevents')
	def on_rminfo_race_norace(self):
		self.fire(RMAnnounceRaceNoRace(), 'announce')

	@handler("RMInfoRaceNoData", channel='infoevents')
	def on_rminfo_race_nodata(self):
		self.fire(RMAnnounceRaceNoData(), 'announce')


	@handler(class RMInfoKartSelected(Event):
	"""Kart selected as target"""


	
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






