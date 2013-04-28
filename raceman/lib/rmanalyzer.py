from circuits.core import Component,Event,handler

RM_PRIO_OOB=0
RM_PRIO_HIGH=1
RM_PRIO_NORMAL=2
RM_PRIO_LOW=3


class RMAnalyzerTarget(Event):
    """Set target kart"""

class RMInfoKartLap(Event):
    """Target kart finished lap"""

class RMInfoKartSelected(Event):
    """Kart selected as target"""

class RMInfoTrackSelected(Event):
    """Track selected as target"""

class RMInfoConnected(Event):
    """Connected to the server"""

class RMAnalyzer(Component):
    """Analyze RMEvent* events and decide what race event user should hear"""

    def __init__(self,*args,**kwargs):
        super(RMAnalyzer,self).__init__(*args,**kwargs)
        self._targettrack=None
        self._targetkart=None


    @handler("rmeventkartlap")
    def _rmeventkartlap(self,kartId,lapTime,sessionTime):
        if self._targetkart and kartId==self._targetkart:
            self.fireEvent(RMInfoKartLap(kartId,lapTime,sessionTime,rmprio=RM_PRIO_HIGH))

    @handler("rmanalyzertarget")
    def _rmanalyzertarget(self,_targettrack,_targetkart):
        self._targetkart=_targetkart
        self._targettrack=_targettrack
        self.fireEvent(RMInfoTrackSelected(_targettrack,rmprio=RM_PRIO_OOB))
        self.fireEvent(RMInfoKartSelected(_targetkart,rmprio=RM_PRIO_OOB))


    @handler("connected")
    def _connected(self,*args,**kwargs):
        self.fireEvent(RMInfoConnected(rmprio=RM_PRIO_OOB))
