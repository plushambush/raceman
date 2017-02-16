from circuits.core import Compoent,handler,Event,Timer
from raceman.lib.focomponent import FOComponent
from raceman.lib.rminfoevents import *

class RaceStateNoData
class RaceStateDataRestored

class RMRaceStateAnnouncer(FOComponent)

	@handler("RMInfoRaceWaiting",channel='infoevents')
	def on_race_waiting(self,raceid):
		if self._state=='UNKNOWN':
			self.change_state('RaceWaiting')
		
	@handler("RMInfoRaceStarted",channel='infoevents')
	def on_race_going(self,raceid):
		if self._state=='RaceWaiting':
			self.change_state('RaceGoing')
			self._hbtimer=Timer(30,RaceStateNoData()).register(self)
			
	@handler("RMInfoRaceHeartBeat",channel='infoevents')
	def on_race_hb(self,raceid):
		if self._state=='RaceWaiting':
			self._hbtimer.reset()
		if self._state=='RaceNoData':
			self.fire(RaceStateDataRestored(),'infoevents')
			