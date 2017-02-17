from circuits.core import Component
import sys

class RMComponent(Component):
	def change_state(self,state):
		self._state=state
		sys.stderr.write ("\n>>> %s changed state to %s  <<<\n\n" % (self.__class__.__name__,state))

	def __init__(self,*args,**kwargs):
		self.change_state('UNKNOWN')
		super(RMComponent,self).__init__(*args,**kwargs)

	
