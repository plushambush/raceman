from circuits.core import Event

class RMInfoConnected(Event):
	"""Conector is connected
	"""	
	channels='infoevents'	
class RMInfoRaceGoing(Event):
	"""Race is started
	"""
	channels='infoevents'
	
class RMInfoRaceStopped(Event):
	"""Race is stopped
	"""
	channels='infoevents'
	
class RMInfoKartLap(Event):
	"""Target kart finished lap
	kartid
	laptime (RacingTime)
	sessiontime (RacingTime)
	"""
	channels='infoevents'	
	name='rminfokartlap'

class RMInfoKartBestLap(Event):
	"""Target kart set best lap"""
	channels='infoevents'	
	name='rminfokartbestlap'

class RMInfoKartLostBestLap(Event):
	"""Kart lost best lap"""
	channels='infoevents'	
	name='rminfokartlostbestlap'    
    
class RMInfoKartLapBetter(Event):
	"""Kart lap time is better then average"""
	channels='infoevents'	
	name='rminfokartlapbetter'

class RMInfoKartLapWorse(Event):
	"""Kart lap time is worse then average"""
	channels='infoevents'	
	name='rminfokartlapworse'

class RMInfoKartSelected(Event):
	"""Kart selected as target"""
	channels='infoevents'	
	name='rminfokartselected'

class RMInfoTrackSelected(Event):
	"""Track selected as target"""
	channels='infoevents'	
	name='rminfotrackselected'

class RMInfoDisconnected(Event):
	"""Disconnected from the server"""
	channels='infoevents'	
	name='rminfodisconnected'

class RMInfoRaceWaiting(Event):
	"""Waiting for race start"""
	channels='infoevents'	
	name='rminforacewaiting'

class RMInfoRaceNoRace(Event):
	"""No race now"""
	channels='infoevents'	
	name='rminforacenorace'

class RMInfoRaceNoData(Event):
	"""No data about race"""
	channels='infoevents'
	name='rminforacenodata'




