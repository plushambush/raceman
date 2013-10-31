#coding=utf-8
# Pattern scanner
# Feed it with data.

class PatternScanner(object):
	def __init__(self,pattern):
		self.reset(pattern)
		
	def scan(self,data):
		self._buffer+=data
		i=self._buffer.find(self._pattern)
		if i<0: #substring not found
			if len(self._buffer)<=self._plen:
				out=''
			else:
				out=self._buffer[0:len(self._buffer)-self._plen]
				self._buffer=self._buffer[len(self._buffer)-self._plen:]
			return (False,out)
			
		else:
			out=self._buffer[0:i]
			self._buffer=self._buffer[i:]
			return (True,out)
	
	def reset(self,pattern=self._pattern):
		self._buffer=''
		self._pattern=pattern
		self._plen=len(pattern)
