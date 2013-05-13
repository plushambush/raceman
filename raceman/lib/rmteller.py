#coding=utf-8
from circuits.core import Component,Event,handler
import raceman.lib.prio

class RMTellSayMessage(Event):
	"""Say text to user"""
	name='rmtellsaymessage'

class RMTellPlayFile(Event):
	"""Play a file to user"""
	name='rmtellplayfile'
	
class RMTellPlayMusic(Event):
	"""Play background music"""
	name='rmtellplaymusic'
	
class RMTellStopMusic(Event):
	"""Stop background music"""
	name='rmtellstopmusic'		

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
		self.fireEvent(RMTellSayMessage(u"   Сле+жение за +каартом   %s." % kart,**kwargs))

	@handler("rminforacewaiting")
	def _rminforacewaiting(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Ожидаем на+чаала гонки.",**kwargs))

	@handler("rminforacegoing")
	def _rminforacegoing(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('gong',**kwargs))
		self.fireEvent(RMTellPlayMusic('',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Гонка нача+лась.",**kwargs))
		

	@handler("rminforacefinish")
	def _rminforacefinish(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('gong',**kwargs))
		self.fireEvent(RMTellStopMusic(**kwargs))
		self.fireEvent(RMTellSayMessage(u"   +Финиш гонки.",**kwargs))

	@handler("rminforacenorace")
	def _rminforacenorace(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   Гонка закончена.",**kwargs))
		

	@handler("rminforacenodata")
	def _rminforacenodata(self,*args,**kwargs):
		self.fireEvent(RMTellSayMessage(u"   С сервера не поступают данные.",**kwargs))


	@handler("rminfokartbestlap")
	def _rminfokartbestlap(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('achv',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Лучшее время гонки.",**kwargs))

	@handler("rminfokartlostbestlap")
	def _rminfokartlostbestlap(self,kartId,kartTime,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('boo',**kwargs))
		self.fireEvent(RMTellSayMessage(u"   Потеряно лучшее время гонки. Карт %s. Время %s" % (kartId,kartTime.tostr(compact=True,tosay=True)),**kwargs))

	@handler("rminfokartlapbetter")
	def _rminfokartlapbetter(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('peew',**kwargs))
		
	@handler("rminfokartlapworse")
	def _rminfokartlapworse(self,*args,**kwargs):
		self.fireEvent(RMTellPlayFile('zzz',**kwargs))
