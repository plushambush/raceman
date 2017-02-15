from circuits.core import Event

class RMInfoConnected(Event):
	"""Conector is connected
	"""	
	
class RMInfoRaceGoing(Event):
	"""Race is started
	"""
	
class RMInfoRaceStopped(Event):
	"""Race is stopped
	"""
	
class RMInfoKartLap(Event):
	"""Target kart finished lap
	kartid
	laptime (RacingTime)
	sessiontime (RacingTime)
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

class RMInfoDisconnected(Event):
	"""Disconnected from the server"""

class RMInfoRaceWaiting(Event):
	"""Waiting for race start"""

class RMInfoRaceNoRace(Event):
	"""No race now"""

class RMInfoRaceNoData(Event):
	"""No data about race"""




