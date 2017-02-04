#coding=utf-8
from circuits.core import Component,Event,handler
from raceman.lib.rmsound_base import *
from raceman.lib.config import *


class RMTeller_SAPI(Component):
	"""Events - Phrases"""

	@handler("rminfokartlap")
	def _rmracelap(self,kartId,lapTime,sessionTime):
		self.fireEvent(RMSoundSayMessage(u"Время круга %s." % lapTime.tostr(compact=True,tosay=True)))


	@handler("rminfoconnected")
	def _connected(self):
		self.fireEvent(RMSoundSayMessage(u"Установлена связь с сервером."))

	@handler("rminfodisconnected")
	def _disconnected(self):
		self.fireEvent(RMSoundSayMessage(u"Разорвана связь с сервером."))

	@handler("rminfotrackselected")
	def _rminfotrackselected(self,track):
		self.fireEvent(RMSoundSayMessage(u"Добро пожаловать на трэк - %s. Устанавливаю связь с сервером." % track))

	@handler("rminfokartselected")
	def _rminfokartselected(self,kart):
		self.fireEvent(RMSoundSayMessage(u"Слежение за картом %s." % kart))

	@handler("rminforacewaiting")
	def _rminforacewaiting(self):
		self.fireEvent(RMSoundSayMessage(u"Ожидаем начала гонки."))

	@handler("rminforacegoing")
	def _rminforacegoing(self):
		self.fireEvent(RMSoundPlayFile(SOUND_STARTSTOP))
		self.fireEvent(RMSoundPlayBGM(SOUND_BGM))
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>началась</emph>!"))
		

	@handler("rminforacefinish")
	def _rminforacefinish(self):
		self.fireEvent(RMSoundPlayFile())
		self.fireEvent(RMSoundStopBGM())
		self.fireEvent(RMSoundSayMessage(u"Финиш гонки!"))

	@handler("rminforacenorace")
	def _rminforacenorace(self):
		self.fireEvent(RMSoundSayMessage(u"Гонка <emph>закончена</emph>."))
		

	@handler("rminforacenodata")
	def _rminforacenodata(self):
		self.fireEvent(RMSoundSayMessage(u"С сервера не поступают данные."))


	@handler("rminfokartbestlap")
	def _rminfokartbestlap(self):
		self.fireEvent(RMSoundPlayFile(SOUND_ACHIEVE))
		self.fireEvent(RMSoundSayMessage(u"Лучшее время гонки!"))

	@handler("rminfokartlostbestlap")
	def _rminfokartlostbestlap(self,kartId,kartTime):
		self.fireEvent(RMSoundPlayFile(SOUND_LOST))
		self.fireEvent(RMSoundSayMessage(u"Потеряно лучшее время гонки. Карт %s Время %s." % (kartId,kartTime.tostr(compact=True,tosay=True))))

	@handler("rminfokartlapbetter")
	def _rminfokartlapbetter(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_GOOD))
		
	@handler("rminfokartlapworse")
	def _rminfokartlapworse(self,avgtime):
		self.fireEvent(RMSoundPlayFile(SOUND_BAD))
