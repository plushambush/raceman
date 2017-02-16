#coding=utf-8
from circuits.core import Component,Event,handler
from raceman.lib.rmsound_base import *
from raceman.lib.config import *

class RMTeller_SAPI(Component):
	"""Events - Phrases"""

	@handler("RMAnnounceKartLap",channel='infoevents')
	def _rmracelap(self,kartId,lapTime,sessionTime):
		self.fireEvent(RMSoundSayMessage(u"Время круга %s." % lapTime.tostr(compact=True,tosay=True)))


	@handler("RMAnnounceConnected",channel='infoevents')
	def _connected(self):
		self.fireEvent(RMSoundSayMessage(u"Установлена связь с сервером."))

	@handler("RMAnnounceDisconnected",channel='infoevents')
	def _disconnected(self):
		self.fireEvent(RMSoundSayMessage(u"Разорвана связь с сервером."))

	@handler("RMAnnounceTrackSelected",channel='infoevents')
	def _rmannouncetrackselected(self,track):
		self.fireEvent(RMSoundSayMessage(u"Добро пожаловать на трэк - %s. Устанавливаю связь с сервером." % track))

	@handler("RMAnnounceTrackSelected",channel='infoevents')
	def _rmannouncekartselected(self,kart):
		self.fireEvent(RMSoundSayMessage(u"Слежение за картом %s." % kart))

	@handler("RMAnnounceRaceWaiting", channel='infoevents')
	def _rmannounceracewaiting(self):
		self.fireEvent(RMSoundSayMessage(u"Ожидаем начала гонки."))

	@handler("RMAnnounceRaceGoing",channel='infoevents')
	def _rmannounceracegoing(self):
		self.fireEvent(RMSoundPlayFile(SOUND_STARTSTOP))
		self.fireEvent(RMSoundPlayBGM(SOUND_BGM))
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>началась</emph>!"))
		

	@handler("RMAnnounceRaceStopped", channel='infoevents')
	def _rmannounceracefinish(self):
		self.fireEvent(RMSoundPlayFile())
		self.fireEvent(RMSoundSayMessage(u"Финиш гонки!"))
		self.fireEvent(RMSoundStopBGM())		

	@handler("RMAnnounceRaceNoRace", channel='infoevents')
	def _rmannounceracenorace(self):
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>закончена</emph>."))
		

	@handler("RMAnnounceRaceNoData", channel='infoevents')
	def _rmannounceracenodata(self):
		self.fireEvent(RMSoundSayMessage(u"С сервера не поступают данные."))


	@handler("RMAnnounceKartBestLap", channel='infoevents')
	def _rmannouncekartbestlap(self):
		self.fireEvent(RMSoundPlayFile(SOUND_ACHIEVE))
		self.fireEvent(RMSoundSayMessage(u"Лучшее время гонки!"))

	@handler("RMAnnounceKartLostBestLap", channel='infoevents')
	def _rmannouncekartlostbestlap(self,kartId,kartTime):
		self.fireEvent(RMSoundPlayFile(SOUND_LOST))
		self.fireEvent(RMSoundSayMessage(u"Потеряно лучшее время гонки. Карт %s Время %s." % (kartId,kartTime.tostr(compact=True,tosay=True))))

	@handler("RMAnnounceKartLapBetter", channel='infoevents')
	def _rmannouncekartlapbetter(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_GOOD))
		
	@handler("RMAnnounceKartLapWorse", channel='infoevents')
	def _rmannouncekartlapworse(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_BAD))
