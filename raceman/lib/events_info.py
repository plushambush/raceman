from circuits.core import Event

class RMInfoRaceStarted(Event):
	"""Race is started
	"""
	
class RMInfoRaceStopped(Event):
	"""Race is stopped
	"""

class RMInfoRaceWaiting(Event):
	"""Waiting for race start"""

class RMInfoRaceNoRace(Event):
	"""No race now"""

class RMInfoRaceNoData(Event):
	"""No data about race"""

class RMInfoRaceHeartBeat(Event):
	"""
	"""
	
class RMInfoKartLap(Event):
	"""Target kart finished lap
	nn,is_target,is_rival,ll,bl,al,self._bbl,pt
	kart num (integer)
	is_target (boolean)
	is_rival (boolean)
	laptime (RacingTime)
	best lap time (RacingTime)
	average time (RacingTime)
	race best lap (RacingTIme)
	Pass time (RacingTime)
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

class RMInfoKartSelected(Event):
	"""Kart selected as target"""

class RMInfoTrackSelected(Event):
	"""Track selected as target"""




