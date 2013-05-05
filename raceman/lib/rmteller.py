#coding=utf-8
from circuits.core import Component,Event,handler
import raceman.lib.prio

class RMTellSayMessage(Event):
	"""Say text to user"""

class RMTellPlayFile(Event):
	"""Play a file to user"""


class RMTeller(Component):
	"""Events - Phrases"""

	@handler("rminfokartlap")
	def _rmracelap(self,kartId,lapTime,sessionTime,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Время круга   %s.  " % lapTime.tostr(compact=True,tosay=True),**kwargs))


	@handler("rminfoconnected")
	def _connected(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Установлено соединение с сервером.",**kwargs))

	@handler("rminfodisconnected")
	def _disconnected(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Соединение с сервером разорвано.",**kwargs))

	@handler("rminfotrackselected")
	def _rminfotrackselected(self,track, *args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Добро пожаловать на трэк   %s." % track,**kwargs))

	@handler("rminfokartselected")
	def _rminfokartselected(self,kart,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Установлено слежение за +каартом   %s." % kart,**kwargs))

	@handler("rminforacewaiting")
	def _rminforacewaiting(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Ожидаем на+чаала гонки.",**kwargs))

	@handler("rminforacegoing")
	def _rminforacegoing(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/gong',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Гонка началась.",**kwargs))

	@handler("rminforacefinish")
	def _rminforacefinish(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/gong',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   +Финиш гонки.",**kwargs))

	@handler("rminforacenorace")
	def _rminforacenorace(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Гонка закончена.",**kwargs))

	@handler("rminforacenodata")
	def _rminforacenodata(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   С сервера не поступают данные.",**kwargs))


	@handler("rminfokartbestlap")
	def _rminfokartbestlap(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/achv',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Установлено лучшее время.",**kwargs))

	@handler("rminfokartlostbestlap")
	def _rminfokartlostbestlap(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/boo',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Потеряно лучшее время.",**kwargs))

	@handler("rminfokartlapbetter")
	def _rminfokartlapbetter(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/peew',**kwargs))
		
	@handler("rminfokartlapworse")
	def _rminfokartlapworse(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('custom/zzz',**kwargs))
		