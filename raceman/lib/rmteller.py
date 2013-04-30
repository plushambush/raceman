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
        self.fireEvent(RMTellSayMessage(u"   Время круга   %s  " % lapTime.tostr(compact=True,tosay=True),kwargs['rmprio']))


    @handler("rminfoconnected")
    def _connected(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Установлено соединение с сервером",kwargs['rmprio']))

    @handler("rminfodisconnected")
    def _disconnected(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Соединение с сервером разорвано",kwargs['rmprio']))

    @handler("rminfotrackselected")
    def _rminfotrackselected(self,track, *args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Добро пожаловать на трэк   %s   " % track,kwargs['rmprio']))

    @handler("rminfokartselected")
    def _rminfokartselected(self,kart,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Установлено слежение за +картом   %s   " % kart,kwargs['rmprio']))

    @handler("rminforacewaiting")
    def _rminforacewaiting(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Ожидаем на+чала гонки",kwargs['rmprio']))

    @handler("rminforacegoing")
    def _rminforacegoing(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Гонка началась",kwargs['rmprio']))

    @handler("rminforacefinish")
    def _rminforacefinish(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Финиш гонки",kwargs['rmprio']))

    @handler("rminforacenorace")
    def _rminforacenorace(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   Гонка закончена",kwargs['rmprio']))

    @handler("rminforacenodata")
    def _rminforacenodata(self,*args,**kwargs):
        self.fireEvent(RMTellSayMessage(u"   С сервера не поступают данные",kwargs['rmprio']))

