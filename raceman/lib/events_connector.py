from circuits.core import Event
class RMConnectorReady(Event):
	""" Connector is ready to be started
	"""

class RMConnectorConfigure(Event):
	"""Configure Connector
	Params
	- config
	- class id
	- kart id
	"""
class RMConnectorStart(Event):
	"""Start connector
	"""
	
class RMConnectorStarted(Event):
	"""Connector started
	"""
