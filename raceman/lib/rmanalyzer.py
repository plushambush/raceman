from circuits.core import Component,Event,handler,Timer
import datetime

RM_PRIO_OOB=0
RM_PRIO_HIGH=1
RM_PRIO_NORMAL=2
RM_PRIO_LOW=3


class RMAnalyzerTarget(Event):
    """Set target kart"""

class RMInfoKartLap(Event):
    """Target kart finished lap"""


class RMInfoKartBestLap(Event):
    """Target kart set best lap"""

class RMInfoKartLostBestLap(Event):
    """Kart lost best lap"""

class RMInfoKartSelected(Event):
    """Kart selected as target"""

class RMInfoTrackSelected(Event):
    """Track selected as target"""

class RMInfoConnected(Event):
    """Connected to the server"""

class RMInfoDisconnected(Event):
    """Disconnected from the server"""

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

class RMTimerNoRaceData(Event):
    """Server not sending data"""


class RMAnalyzer(Component):
    """Analyze RMEvent* events and decide what race event user should hear"""

    def __init__(self,*args,**kwargs):
        super(RMAnalyzer,self).__init__(*args,**kwargs)
        self._targettrack=None
        self._targetkart=None
        self._racestatus=None
        self._racestatustime=None
        self._racebestlap=None
        self._racebesttime=None
        self._racehavebesttime=False
        self._datatimer=Timer(s=20,e=RMTimerNoRaceData(),persist=True,c="rmtimernoracedata").register(self)

    def _isTargetKart(self,kartId):
        return (self._targetkart is not None) and (self._targetkart==kartId)

    @handler("rmeventkartlap")
    def _rmeventkartlap(self,kartId,lapTime,sessionTime):
        if self._targetkart and self._isTargetKart(kartId):
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


    @handler("disconnected")
    def _disconnected(self,*args,**kwargs):
        self.fireEvent(RMInfoDisconnected(rmprio=RM_PRIO_OOB))


    @handler("rmeventheartbeat")
    def _rechargedatatimer(self,*args,**kwargs):
        self._datatimer.reset()

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

        self._updateracestatus(status)

    @handler("rmtimernoracedata")
    def _rmtimernoracedata(self,*args,**kwargs):
        self.fireEvent(RMInfoRaceNoData(rmprio=RM_PRIO_LOW))

    def _updateracestatus(self,status):
        if status<>self._racestatus:
            self._racestatus=status
            self._racestatustime=datetime.datetime.now()
            self._tellracestatus(status,RM_PRIO_OOB)
        elif (datetime.datetime.now()-self._racestatustime)>datetime.timedelta(minutes=1) and self._racestatus<>"RACE":
            self._racestatustime=datetime.datetime.now()
            self._tellracestatus(self._racestatus,RM_PRIO_LOW)        

    def _tellracestatus(self,status,prio):
        statevents={'WAITING':RMInfoRaceWaiting,'RACE':RMInfoRaceGoing,'FINISH':RMInfoRaceFinish,'NORACE':RMInfoRaceNoRace}    
        event=statevents[status]
        self.fireEvent(event(rmprio=prio))
        

    @handler("rmeventkartplacetime")
    def _rmeventkartplacetime(self,place,kartId,lap,lapTime,unk1):
        if place==1:
            if self._isTargetKart(kartId):
                if not self._racehavebesttime:
                    self.fireEvent(RMInfoKartBestLap(rmprio=RM_PRIO_NORMAL))
                    self._racebestlap=lap
                    self._racebesttime=lapTime
                    self._racehavebesttime=True
            else:
                if self._racehavebesttime:
                    self._racehavebesttime=False
                    self._racebesttime=lapTime
                    self._racebestlap=lap
                    self.fireEvent(RMInfoKartLostBestLap(rmprio=RM_PRIO_NORMAL))
