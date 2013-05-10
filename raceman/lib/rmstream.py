from circuits.core import Event, Component, handler

class RMStreamEvent(Event):
	"""Data received from the server"""
	name='rmstreamevent'

class RMStreamEventBadData(Event):
	"""Wrongly formatted data received from server"""
	name='rmstreameventbaddata'

class RMStream(Component):
  """Receive data from server"""

  @handler("line")
  def _line(self,*args, **kwargs):
    comps=[comp.strip("\" .") for comp in args[0].split(",")]
    if (len(comps)>0):
      if (comps[0][0]=="$"):
        self.fireEvent(RMStreamEvent(*comps))
        return
    self.fireEvent(RMStreamEventBadData(*args))

