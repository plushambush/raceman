from circuits.core import Component
import sys

class RMComponent(Component):
	def change_state(self,state):
		self._state=state
		sys.stderr.write ("\n>>> %s changed state to %s  <<<\n\n" % (self.__class__.__name__,state))

	def push_state(self,state):
		self._statestack.append(self._state)
		self.change_state(state)
		
	def pop_state(self,):
		st=self._statestack.pop()
		self.change_state(st)

	def __init__(self,*args,**kwargs):
		self._statestack=[]
		self.change_state('UNKNOWN')
		super(RMComponent,self).__init__(*args,**kwargs)

	
	def debug(self,s):
		sys.stderr.write(str)