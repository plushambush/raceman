from circuits.core import Component,Event,handler
from raceman.lib.racingtime import RacingTime


class RMEventHeartBeat(Event):
    """F event (heartbeat every second)"""

class RMEventKartLap(Event):
    """J event: kart passes finish line"""


class RMEventKartPlaceTime(Event):
    """SP event: kart place (by time)"""


class RMEventUnknown(Event):
  """Unknown command  received from the stream, cannot decode"""

class RMDecoder(Component):
  """Decoder of the data received from server"""




  @handler("rmstreamevent")
  def _rmstreamevent(self,*args,**kwargs):
    command="_interpret_" + (args[0][1:]).upper()
    if hasattr(self,command) and callable(getattr(self,command)):
        getattr(self,command)(*args[1:])
    else:
        self.push(RMEventUnknown(args))

  def _interpret_F(self,*args,**kwargs):
    """interpret $F command
    $F,0,"00:06:36","14:27:38","00:00:23","Green ".
    lapsToGo
    timeToGo
    currentTime
    sessionTime
    flagStatus"""

    self.push(RMEventHeartBeat(lapsToGo=int(args[0]),
            timeToGo=args[1],
            currentTime=args[2],
            sessionTime=args[3],
            flagStatus=args[4]))


  def _interpret_J(self,*args,**kwargs):
    """interpret $J command
        $J,"3","00:00:40.179","00:02:07.037".
        id
        LapTime
        sessionTime
    """
    if args[1]<>"00:00:00":
    	self.push(RMEventKartLap(kartId=args[0],lapTime=RacingTime.fromstr(args[1]),sessionTime=RacingTime.fromstr(args[2])))


  def _interpret_SP(self,*args,**kwargs):
    """ interpret SP command
    $SP,2,"10",1,"00:00:45.087",35930.
    place
    kartId
    lapNo
    lapTime
    unk1"""
    self.push(RMEventKartPlaceTime(int(args[0]), unicode(args[1]), int(args[2]), RacingTime.fromstr(args[3]),args[4]))
