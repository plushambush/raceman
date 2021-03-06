#coding=utf-8
from circuits.core import handler,Event
from raceman.lib.eventqueue import EventQueue,EQEnqueueEvent,EQHandler,EQHandlerAvailable
from raceman.lib.rmagi import AGICommand

class RMAGICommand(Event):
	"""AGI Command"""
	name='rmagicommand'

class RMAGISound(EventQueue):
	@handler("rmtellsaymessage")
	def _rmtellsaymessage(self,phrase,rmprio):
		self.fireEvent(EQEnqueueEvent(AGICommand(u"EXEC FESTIVAL \"%s\"" % phrase),rmprio))

	@handler("rmtellplayfile")
	def _rmtellplayfile(self,_file,rmprio):
		self.fireEvent(EQEnqueueEvent(AGICommand(u"STREAM FILE custom/%s any" % _file),rmprio))

#	@handler("rmtellplaymusic")
#	def _rmtellplaymusic(self,music,rmprio):
#		self.fireEvent(EQEnqueueEvent(AGICommand(u"SET MUSIC on raceman" ),rmprio))

#	@handler("rmtellstopmusic")
#	def _rmtellstopmusic(self,rmprio):
#		self.fireEvent(EQEnqueueEvent(AGICommand(u"SET MUSIC off"),rmprio))

class RMAGIHandler(EQHandler):
	@handler("agistartupcomplete")
	def _onrmagistartupcomplete(self,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(self))

	@handler("rmagicommand")
	def _onrmagicommand(self,*args,**kwargs):
		self.fireEvent(AGICommand(*args,**kwargs))


	@handler("agiready")
	def _onagiready(self,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(self))
        