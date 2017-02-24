# -*- coding: utf-8 -*-
from circuits.core import Component,Event,handler
from raceman.lib.sound_base import *
from raceman.lib.config  import *
from raceman.lib.racingtime import RacingTime

class RMTeller_SAPI(Component):
	"""Events - Phrases"""

	@handler("RMAnnounceTargetLap",channel='announce')
	def _rmracelap(self,kartId,lapTime,sessionTime):
		if lapTime<>RacingTime.fromint(0):
			self.fire(RMSoundSayMessage(u"Время круга %s." % lapTime.round(config.profile['TIME_PRECISION']).say()))

	@handler("RMAnnounceRivalLap",channel='announce')
	def _rmrace_rival_lap(self,kartId,lapTime,sessionTime):
		if lapTime<>RacingTime.fromint(0):
			self.fire(RMSoundSayMessage(u"Время соперника %s." % lapTime.round(config.profile['TIME_PRECISION']).say()))

	@handler("RMAnnounceConnected",channel='announce')
	def _connected(self):
		self.fireEvent(RMSoundSayMessage(u"Установлена связь с сервером."))

	@handler("RMAnnounceDisconnected",channel='announce')
	def _disconnected(self):
		self.fireEvent(RMSoundSayMessage(u"Разорвана связь с сервером."))

	@handler("RMAnnounceTrackSelected",channel='announce')
	def _rmannouncetrackselected(self,track):
		self.fireEvent(RMSoundSayMessage(u"Добро пожаловать на трэк  %s." % track))

	@handler("RMAnnounceKartSelected",channel='announce')
	def _rmannouncekartselected(self,kart):
		self.fireEvent(RMSoundSayMessage(u"Слежение за картом %s." % kart))
		
	@handler("RMAnnounceRivalSelected",channel='announce')
	def _rmannouncerivalselected(self,kart):
		self.fireEvent(RMSoundSayMessage(u"Соперник карт  %s." % kart))		

	@handler("RMAnnounceRaceWaiting", channel='announce')
	def _rmannounceracewaiting(self):
		self.fireEvent(RMSoundSayMessage(u"Ожидаем начала гонки."))

	@handler("RMAnnounceRaceStarted",channel='announce')
	def _rmannounceracestarted(self,raceid):
		self.fireEvent(RMSoundPlayFile(SOUND_STARTSTOP))
		self.fireEvent(RMSoundPlayBGM(SOUND_BGM))
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>началась</emph>!"))
		

	@handler("RMAnnounceRaceStopped", channel='announce')
	def _rmannounceracestopped(self):
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>закончена</emph>."))
		self.fireEvent(RMSoundStopBGM())		

	@handler("RMAnnounceRaceNoRace", channel='announce')
	def _rmannounceracenorace(self):
		self.fireEvent(RMSoundSayMessage(u"Сейчас нет гонки."))
		

	@handler("RMAnnounceRaceNoData", channel='announce')
	def _rmannounceracenodata(self):
		self.fireEvent(RMSoundSayMessage(u"С сервера перестали поступать данные."))

	@handler("RMAnnounceRaceDataBack", channel='announce')
	def _rmannounceracedataback(self):
		self.fireEvent(RMSoundSayMessage(u"Данные снова поступают."))


	@handler("RMAnnounceKartBestLap", channel='announce')
	def _rmannouncekartbestlap(self):
		self.fireEvent(RMSoundPlayFile(SOUND_ACHIEVE))
		self.fireEvent(RMSoundSayMessage(u"Лучшее время гонки!"))

	@handler("RMAnnounceKartLostBestLap", channel='announce')
	def _rmannouncekartlostbestlap(self,kartId,kartTime):
		self.fireEvent(RMSoundPlayFile(SOUND_LOST))
		self.fire(RMSoundSayMessage(u"Потеряно лучшее время гонки. Карт %s Время %s." % (kartId,kartTime.say())))

	@handler("RMAnnounceKartLapBetter", channel='announce')
	def _rmannouncekartlapbetter(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_GOOD))
		
	@handler("RMAnnounceKartLapWorse", channel='announce')
	def _rmannouncekartlapworse(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_BAD))
