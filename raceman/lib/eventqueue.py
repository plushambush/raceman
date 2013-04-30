from circuits.core import Component,Event,handler
from raceman.lib.rmqueue import RMQueue,RMQItem
import Queue


class EQHaveEvent(Event):
    """Fired when EventQueue has new event"""

class EQEmpty(Event):
    """Fired when EventQueue is empty"""


class EQFull(Event):
    """Fired when EventQueue is full"""

class EQHandlerBusy(Event):
    """Fired when Handler is busy"""

class EQEnqueueEvent(Event):
    """Receive an event apd put it in queue"""

class EQHandlerAvailable(Event):
    """Sent by an available handler"""

class EQHandlerEngaged(Event):
    """Sent by handler when it's waiting for event"""

class EventQueue(Component):
    """Event Queue"""
    def __init__(self,*args,**kwargs):
        super(EventQueue,self).__init__(args,kwargs)
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
        super(EQHandler,self).__init__(args,kwargs)
        self._free=False

    @handler("eqhaveevent")
    def _on_eqhaveevent(self,_event,_priority,*args,**kwargs):
        if self._free:
            self._free=False
            self.fireEvent(EQHandlerEngaged(self,_event))
        else:
            self.fireEvent(EQHandlerBusy(self,_event))

    @handler("eqhandleravailable",priority=100)
    def _on_eqhandleravailable(self,*args,**kwargs):
        self._free=True

