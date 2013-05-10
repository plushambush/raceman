from circuits.core import Component,Event,handler,Timer
import datetime
from raceman.lib.prio import *
import re

class RMAnalyzerTarget(Event):
	"""Set target kart"""
	name='rmanalyzertarget'

class RMInfoKartLap(Event):
	"""Target kart finished lap"""
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

class RMInfoConnected(Event):
	"""Connected to the server"""
	name='rminfoconnected'

class RMInfoDisconnected(Event):
	"""Disconnected from the server"""
	name='rminfodisconnected'

class RMInfoRaceWaiting(Event):
	"""Waiting fir race start"""
	name='rminforacewaiting'

class RMInfoRaceGoing(Event):
	"""Race is started"""
	name='rminforacegoing'

class RMInfoRaceFinish(Event):
	"""Race is finished"""
	name='rminforacefinish'

class RMInfoRaceNoRace(Event):
	"""No race now"""
	name='rminforacenorace'

class RMInfoRaceNoData(Event):
	"""No data about race"""
	name='rminforacenodata'

class RMTimerNoRaceData(Event):
	"""Server not sending data"""
	name='rmtimernoracedata'

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
