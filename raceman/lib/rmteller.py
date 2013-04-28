#coding=utf-8
from circuits.core import Component,Event,handler


class RMTellSayMessage(Event):
    """Say text to user"""

class RMTellPlayFile(Event):
    """Play a file to user"""


class RMTeller(Component):
    """Events - Phrases"""

    @handler("rminfokartlap")
    def _rmracelap(self,kartId,lapTime,sessionTime,*args,**kwargs):
        self.fireEvent(RMTellPlayFile("beep",kwargs['rmprio']))
        self.fireEvent(RMTellSayMessage(u"Время круга   %s  " % lapTime.tostr(compact=True,tosay=True),kwargs['rmprio']))


    @handler("rminfoconnected")
    def _connected(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Установлено соединение с сервером",kwargs['rmprio']))

    @handler("rminfotrackselected")
    def _rminfotrackselected(self,track, *args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Добро пожаловать на трек   %s   " % track,kwargs['rmprio']))

    @handler("rminfokartselected")
    def _rminfokartselected(self,kart,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Установлено слежение за картом   %s   " % kart,kwargs['rmprio']))
