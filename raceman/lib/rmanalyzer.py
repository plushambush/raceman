from circuits.core import Component,Event,handler
import datetime

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

class RMInfoRaceWaiting(Event):
    """Waiting fir race start"""

class RMInfoRaceGoing(Event):
    """Race is started"""

class RMInfoRaceFinish(Event):
    """Race is finished"""

class RMInfoRaceNoRace(Event):
    """No race now"""

class RMInfoRaceNoData(Event):
    """No data about race"""


class RMAnalyzer(Component):
    """Analyze RMEvent* events and decide what race event user should hear"""

    def __init__(self,*args,**kwargs):
        super(RMAnalyzer,self).__init__(*args,**kwargs)
        self._targettrack=None
        self._targetkart=None
        self._racestatus=None
        self._racestatustime=None


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


    @handler("rmeventheartbeat")
    def _heartbeat(self,lapsToGo,timeToGo,currentTime,sessionTime,flagStatus):

        if flagStatus=="Green":
            if sessionTime<>"00:00:00":
                status="RACE"
            else:
                status="WAITING"
        elif flagStatus=="Finish":
            status="FINISH"
        else:
            status="NORACE"
        
        if status<>self._racestatus:
            self._racestatus=status
            self._racestatustime=datetime.datetime.now()
            self._tellracestatus(status,RM_PRIO_HIGH)
        elif (datetime.datetime.now()-self._racestatustime)>datetime.timedelta(minutes=1) and self._racestatus<>"RACE":
            self._racestatustime=datetime.datetime.now()
            self._tellracestatus(self._racestatus,RM_PRIO_LOW)

    def _tellracestatus(self,status,prio):
        statevents={'WAITING':RMInfoRaceWaiting,'RACE':RMInfoRaceGoing,'FINISH':RMInfoRaceFinish,'NORACE':RMInfoRaceNoRace, 'NODATA':RMInfoRaceNoData}    
        event=statevents[status]
        self.fireEvent(event(rmprio=prio))
        