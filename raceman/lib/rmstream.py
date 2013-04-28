from circuits.core import Event, Component, handler

class RMStreamEvent(Event):
  """Data received from the server"""

class RMStreamEventBadData(Event):
  """Wrongly formatted data received from server"""

class RMStream(Component):
  """Receive data from server"""

  @handler("line",channel="datastream")
  def _line(self,*args, **kwargs):
    comps=[comp.strip("\" .") for comp in args[0].split(",")]
    if (len(comps)>0):
      if (comps[0][0]=="$"):
        self.fireEvent(RMStreamEvent(*comps))
        return
    self.fireEvent(RMStreamEventBadData(args))

