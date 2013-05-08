from circuits.core import Component,Event,handler,Timer
import datetime
from raceman.lib.prio import *
import re

class RMAnalyzerTarget(Event):
	name='rmanalyzertarget'
	"""Set target kart"""

class RMInfoKartLap(Event):
	name='rminfokartlap'
	"""Target kart finished lap"""


class RMInfoKartBestLap(Event):
	name='rminfokartbestlap'
	"""Target kart set best lap"""

class RMInfoKartLostBestLap(Event):
	name='rminfokartlostbestlap'
	"""Kart lost best lap"""
    
class RMInfoKartLapBetter(Event):
	name='rminfokartlapbetter'
	"""Kart lap time is better then average"""

class RMInfoKartLapWorse(Event):
	name='rminfokartlapworse'
	"""Kart lap time is worse then average"""

class RMInfoKartSelected(Event):
	name='rminfokartselected'
	"""Kart selected as target"""

class RMInfoTrackSelected(Event):
	name='rminfotrackselected'
	"""Track selected as target"""

class RMInfoConnected(Event):
	name='rminfoconnected'
	"""Connected to the server"""

class RMInfoDisconnected(Event):
	name='rminfodisconnected'
	"""Disconnected from the server"""

class RMInfoRaceWaiting(Event):
	name='rminforacewaiting'
	"""Waiting fir race start"""

class RMInfoRaceGoing(Event):
	name='rminforacegoing'
	"""Race is started"""

class RMInfoRaceFinish(Event):
	name='rminforacefinish'
	"""Race is finished"""

class RMInfoRaceNoRace(Event):
	name='rminforacenorace'
	"""No race now"""

class RMInfoRaceNoData(Event):
	name='rminforacenodata'
	"""No data about race"""

class RMTimerNoRaceData(Event):
	name='rmtimernoracedata'
	"""Server not sending data"""


class RMAnalyzer(Component):
	"""Analyze RMEvent* events and decide what race event user should hear"""

	def __init__(self,*args,**kwargs):
		super(RMAnalyzer,self).__init__(*args,**kwargs)
		self._targettrack=None
		self._targetkart=None
		self._racestatus=None
		self._racestatustime=None
		self._datatimer=Timer(20,RMTimerNoRaceData(),persist=True,c="rmtimernoracedata").register(self)
		self._clearracedata()
		
		
	def _clearracedata(self):
		self._racebestlap=None
		self._racebesttime=None
		self._racehavebesttime=False
		self._kartavgtime=None
		
	
	def _isTargetKart(self,kartId):
		 return (self._targetkart is not None) and (self._targetkart.match(kartId))

	@handler("rmeventkartlap",priority=50)
	def _rmeventkartlap1(self,kartId,lapTime,sessionTime):
		if self._isTargetKart(kartId):
			if self._kartavgtime:
				if lapTime<=self._kartavgtime:
					self.fireEvent(RMInfoKartLapBetter(self._kartavgtime,rmprio=RM_PRIO_HIGH))
				else:
					self.fireEvent(RMInfoKartLapWorse(self._kartavgtime,rmprio=RM_PRIO_HIGH))
				self._kartavgtime=(self._kartavgtime+lapTime)/2
			else:
				self._kartavgtime=lapTime
	
	
	
	@handler("rmeventkartlap",priority=40)
	def _rmeventkartlap(self,kartId,lapTime,sessionTime):
		if self._targetkart and self._isTargetKart(kartId):
			self.fireEvent(RMInfoKartLap(kartId,lapTime,sessionTime,rmprio=RM_PRIO_HIGH))

	@handler("rmanalyzertarget")
	def _rmanalyzertarget(self,_targettrack,_targetkart,_targetkartname):
		self._targetkart=re.compile(_targetkart)
		self._targettrack=_targettrack
		self.fireEvent(RMInfoTrackSelected(_targettrack,rmprio=RM_PRIO_OOB))
		self.fireEvent(RMInfoKartSelected(_targetkartname,rmprio=RM_PRIO_OOB))


	@handler("connected")
	def _connected(self,*args,**kwargs):
		self.fireEvent(RMInfoConnected(rmprio=RM_PRIO_OOB))


	@handler("disconnected")
	def _disconnected(self,*args,**kwargs):
		self.fireEvent(RMInfoDisconnected(rmprio=RM_PRIO_OOB))


	@handler("rmeventheartbeat")
	def _rechargedatatimer(self,*args,**kwargs):
		self._datatimer.reset()

	@handler("rmeventheartbeat")
	def _heartbeat(self,lapsToGo,timeToGo,currentTime,sessionTime,flagStatus):
		if flagStatus=="Green":
			if sessionTime<>"00:00:00":
				status="RACE"
			else:
				status="WAITING"
		elif flagStatus=="Finish":
			status="FINISH"
		else:
			status="NORACE"
			self._clearracedata()
		self._updateracestatus(status)

	@handler("rmtimernoracedata")
	def _rmtimernoracedata(self,*args,**kwargs):
		self.fireEvent(RMInfoRaceNoData(rmprio=RM_PRIO_LOW))

	def _updateracestatus(self,status):
		if status<>self._racestatus:
			self._racestatus=status
			self._racestatustime=datetime.datetime.now()
			self._tellracestatus(status,RM_PRIO_OOB)
		elif (datetime.datetime.now()-self._racestatustime)>datetime.timedelta(minutes=1) and self._racestatus<>"RACE":
			self._racestatustime=datetime.datetime.now()
			self._tellracestatus(self._racestatus,RM_PRIO_LOW)        

	def _tellracestatus(self,status,prio):
		statevents={'WAITING':RMInfoRaceWaiting,'RACE':RMInfoRaceGoing,'FINISH':RMInfoRaceFinish,'NORACE':RMInfoRaceNoRace}    
		event=statevents[status]
		self.fireEvent(event(rmprio=prio))

	@handler("rmeventkartplacetime")
	def _rmeventkartplacetime(self,place,kartId,lap,lapTime,unk1):
		if place==1:
			if self._isTargetKart(kartId):
				if (not self._racebesttime) or lapTime<self._racebesttime:
					self.fireEvent(RMInfoKartBestLap(rmprio=RM_PRIO_NORMAL))
					self._racebestlap=lap
					self._racebesttime=lapTime
					self._racehavebesttime=True
			else:
				if self._racehavebesttime:
					self._racehavebesttime=False
					self._racebesttime=lapTime
					self._racebestlap=lap
					self.fireEvent(RMInfoKartLostBestLap(rmprio=RM_PRIO_NORMAL))
