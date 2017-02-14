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
	name='rminfokartlap'

class RMInfoKartBestLap(Event):
	"""Target kart set best lap"""
	name='rminfokartbestlap'

class RMInfoKartLostBestLap(Event):
	"""Kart lost best lap"""
	name='rminfokartlostbestlap'    
    
class RMInfoKartLapBetter(Event):
	"""Kart lap time is better then average"""
	name='rminfokartlapbetter'

class RMInfoKartLapWorse(Event):
	"""Kart lap time is worse then average"""
	name='rminfokartlapworse'

class RMInfoKartSelected(Event):
	"""Kart selected as target"""
	name='rminfokartselected'

class RMInfoTrackSelected(Event):
	"""Track selected as target"""
	name='rminfotrackselected'

class RMInfoDisconnected(Event):
	"""Disconnected from the server"""
	name='rminfodisconnected'

class RMInfoRaceWaiting(Event):
	"""Waiting for race start"""
	name='rminforacewaiting'

class RMInfoRaceNoRace(Event):
	"""No race now"""
	name='rminforacenorace'

class RMInfoRaceNoData(Event):
	"""No data about race"""
	name='rminforacenodata'




