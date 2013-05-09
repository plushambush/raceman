from circuits.core import Event, Component, handler

class RMStreamEvent(Event):
	name='rmstreamevent'
	"""Data received from the server"""

class RMStreamEventBadData(Event):
	name='rmstreameventbaddata'
	"""Wrongly formatted data received from server"""

class RMStream(Component):
  """Receive data from server"""

  @handler("line")
  def _line(self,*args, **kwargs):
    comps=[comp.strip("\" .") for comp in args[0].split(",")]
    if (len(comps)>0):
      if (comps[0][0]=="$"):
        self.fireEvent(RMStreamEvent(*comps))
        return
    self.fireEvent(RMStreamEventBadData(args))

