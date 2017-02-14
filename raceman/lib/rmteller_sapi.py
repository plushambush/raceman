#coding=utf-8
from circuits.core import Component,Event,handler
from raceman.lib.rmsound_base import *
from raceman.lib.config import *


class RMTeller_SAPI(Component):
	"""Events - Phrases"""

	@handler("RMInfoKartLap",channel='infoevents')
	def _rmracelap(self,kartId,lapTime,sessionTime):
		self.fireEvent(RMSoundSayMessage(u"Время круга %s." % lapTime.tostr(compact=True,tosay=True)))


	@handler("RMInfoConnected",channel='infoevents')
	def _connected(self):
		self.fireEvent(RMSoundSayMessage(u"Установлена связь с сервером."))

	@handler("RMInfoDisconnected",channel='infoevents')
	def _disconnected(self):
		self.fireEvent(RMSoundSayMessage(u"Разорвана связь с сервером."))

	@handler("RMInfoTrackSelected",channel='infoevents')
	def _rminfotrackselected(self,track):
		self.fireEvent(RMSoundSayMessage(u"Добро пожаловать на трэк - %s. Устанавливаю связь с сервером." % track))

	@handler("RMInfoTrackSelected",channel='infoevents')
	def _rminfokartselected(self,kart):
		self.fireEvent(RMSoundSayMessage(u"Слежение за картом %s." % kart))

	@handler("RMInfoRaceWaiting", channel='infoevents')
	def _rminforacewaiting(self):
		self.fireEvent(RMSoundSayMessage(u"Ожидаем начала гонки."))

	@handler("RMInfoRaceGoing",channel='infoevents')
	def _rminforacegoing(self):
		self.fireEvent(RMSoundPlayFile(SOUND_STARTSTOP))
		self.fireEvent(RMSoundPlayBGM(SOUND_BGM))
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>началась</emph>!"))
		

	@handler("RMInfoRaceFinish", channel='infoevents')
	def _rminforacefinish(self):
		self.fireEvent(RMSoundPlayFile())
		self.fireEvent(RMSoundStopBGM())
		self.fireEvent(RMSoundSayMessage(u"Финиш гонки!"))

	@handler("RMInfoRaceNoRace", channel='infoevents')
	def _rminforacenorace(self):
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>закончена</emph>."))
		

	@handler("RMInfoRaceNoData", channel='infoevents')
	def _rminforacenodata(self):
		self.fireEvent(RMSoundSayMessage(u"С сервера не поступают данные."))


	@handler("RMInfoKartBestLap", channel='infoevents')
	def _rminfokartbestlap(self):
		self.fireEvent(RMSoundPlayFile(SOUND_ACHIEVE))
		self.fireEvent(RMSoundSayMessage(u"Лучшее время гонки!"))

	@handler("RMInfoKartLostBestLap", channel='infoevents')
	def _rminfokartlostbestlap(self,kartId,kartTime):
		self.fireEvent(RMSoundPlayFile(SOUND_LOST))
		self.fireEvent(RMSoundSayMessage(u"Потеряно лучшее время гонки. Карт %s Время %s." % (kartId,kartTime.tostr(compact=True,tosay=True))))

	@handler("RMInfoKartLapBetter", channel='infoevents')
	def _rminfokartlapbetter(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_GOOD))
		
	@handler("RMInfoKartLapWorse", channel='infoevents')
	def _rminfokartlapworse(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_BAD))
