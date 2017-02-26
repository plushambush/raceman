# -*- coding: utf-8 -*-
from circuits.core import Component,Event,handler
from raceman.lib.sound_base import *
from raceman.lib.config  import *
from raceman.lib.racingtime import RacingTime
from raceman.lib.numberspell_static import spell

class RMTeller_Static(Component):
	"""Events - Phrases"""

	@handler("RMAnnounceTargetLap",channel='announce')
	def _rmracelap(self,kartId,lapTime,sessionTime):
		if lapTime<>RacingTime.fromint(0):
			self.fire(RMSoundPlayArray(['time']+ lapTime.round(config.profile['TIME_PRECISION']).say_list()))

	@handler("RMAnnounceRivalLap",channel='announce')
	def _rmrace_rival_lap(self,kartId,lapTime,sessionTime):
		if lapTime<>RacingTime.fromint(0):
			self.fire(RMSoundPlayArray(['rivaltime']+ lapTime.round(config.profile['TIME_PRECISION']).say_list()))

	@handler("RMAnnounceConnected",channel='announce')
	def _connected(self):
		self.fireEvent(RMSoundPlayArray(['connected']))

	@handler("RMAnnounceDisconnected",channel='announce')
	def _disconnected(self):
		self.fireEvent(RMSoundPlayArray(['disconnected']))

	@handler("RMAnnounceTrackSelected",channel='announce')
	def _rmannouncetrackselected(self,track):
		self.fireEvent(RMSoundPlayArray(['trackselected',config.track['spell']]))

	@handler("RMAnnounceKartSelected",channel='announce')
	def _rmannouncekartselected(self,kart):
		self.fireEvent(RMSoundPlayArray(['kartselected']+spell(kart)))
		
	@handler("RMAnnounceRivalSelected",channel='announce')
	def _rmannouncerivalselected(self,kart):
		self.fireEvent(RMSoundPlayArray(['rivalselected']+spell(kart)))

	@handler("RMAnnounceRaceWaiting", channel='announce')
	def _rmannounceracewaiting(self):
		self.fireEvent(RMSoundPlayArray(['racewaiting']))

	@handler("RMAnnounceRaceStarted",channel='announce')
	def _rmannounceracestarted(self,raceid):
		self.fireEvent(RMSoundPlayFile(SOUND_STARTSTOP))
		self.fireEvent(RMSoundPlayBGM(SOUND_BGM))
		self.fireEvent(RMSoundPlayArray(['racestarted']))
		

	@handler("RMAnnounceRaceStopped", channel='announce')
	def _rmannounceracestopped(self):
		self.fireEvent(RMSoundPlayArray(['racefinished']))
		self.fireEvent(RMSoundStopBGM())		

	@handler("RMAnnounceRaceNoRace", channel='announce')
	def _rmannounceracenorace(self):
		self.fireEvent(RMSoundPlayArray(['norace']))
		

	@handler("RMAnnounceRaceNoData", channel='announce')
	def _rmannounceracenodata(self):
		self.fireEvent(RMSoundPlayArray(['nodata']))

	@handler("RMAnnounceRaceDataBack", channel='announce')
	def _rmannounceracedataback(self):
		self.fireEvent(RMSoundPlayAray(['dataagain']))


	@handler("RMAnnounceKartBestLap", channel='announce')
	def _rmannouncekartbestlap(self):
		self.fireEvent(RMSoundPlayFile(SOUND_ACHIEVE))
		self.fireEvent(RMSoundPlayArray(['bestlap']))

	@handler("RMAnnounceKartLostBestLap", channel='announce')
	def _rmannouncekartlostbestlap(self,kartId,kartTime):
		self.fireEvent(RMSoundPlayFile(SOUND_LOST))
		self.fire(RMSoundPlayArray(['lostbestlap','kart'] + spell(kartId) + ['time'] + kartTime.say_list()))

	@handler("RMAnnounceKartLapBetter", channel='announce')
	def _rmannouncekartlapbetter(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_GOOD))
		
	@handler("RMAnnounceKartLapWorse", channel='announce')
	def _rmannouncekartlapworse(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_BAD))
