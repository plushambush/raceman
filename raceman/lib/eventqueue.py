from circuits.core import Component,Event,handler
from raceman.lib.rmqueue import RMQueue,RMQItem
import Queue
import sys


class EQHaveEvent(Event):
	"""Fired when EventQueue has new event"""
	name='eqhaveevent'

class EQEmpty(Event):
	"""Fired when EventQueue is empty"""
	name='eqempty'

class EQFull(Event):
	"""Fired when EventQueue is full"""
	name='eqfull'


class EQHandlerBusy(Event):

	name='eqhandlerbusy'


class EQEnqueueEvent(Event):
	"""Receive an event and put it in queue"""
	name='eqenqueueevent'

class EQHandlerAvailable(Event):
	"""Sent by an available handler"""
	name='eqhandleravailable'

class EQHandlerEngaged(Event):
	"""Sent by handler when it's waiting for event"""
	name='eqhandlerengaged'

class EventQueue(Component):
	"""Event Queue"""
	def __init__(self,*args,**kwargs):
		super(EventQueue,self).__init__(*args,**kwargs)
		self._equeue=RMQueue()


	@handler("eqenqueueevent")
	def _on_enqueueevent(self,_event,_priority):
		try:
			self._equeue.put_nowait(RMQItem(_event,priority=_priority))
			self.fireEvent(EQHaveEvent(_event,_priority))
		except Queue.Full:
			self.fireEvent(EQFull())

	@handler("eqhandleravailable")
	def _on_eqhandleravailable(self,*args,**kwargs):
		if not self._equeue.empty():
			self.fireEvent(EQHaveEvent(None,None))


	@handler("eqhandlerengaged")
	def _on_eqhandlerengaged(self,*args,**kwargs):
		try:
			item=self._equeue.get_nowait()
			self.fireEvent(item.value)
			self._equeue.task_done()
		except Queue.Empty:
			self.fireEvent(EQEmpty())



class EQHandler(Component):
	"""Event handler compatible with EventQueue"""
	def __init__(self,*args,**kwargs):
		super(EQHandler,self).__init__(*args,**kwargs)
		self._free=False

	@handler("eqhaveevent")
	def _on_eqhaveevent(self,_event,_priority,*args,**kwargs):
		if self._free:
			self._free=False
			self.fireEvent(EQHandlerEngaged(self,_event))
		else:
			self.fireEvent(EQHandlerBusy(self,_event))

	@handler("eqhandleravailable",priority=sys.maxint)
	def _on_eqhandleravailable(self,*args,**kwargs):
		self._free=True

