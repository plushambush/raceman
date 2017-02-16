from circuits import handler,Component,Event
from raceman.lib.config import *
import md5
import os.path

class RMTTSConvertMessage(Event):
	pass

class RMTTS(Component):
	def __init__(self,*args,**kwargs):
		super(RMTTS,self).__init__(*args,**kwargs)
		self.cache_prefix='TTS'
		
	def cachefile_name(self,message):
		m = md5.new()
		m.update(message.encode('windows-1251'))
		return TTS_CACHE_DIR + '/' + self.cache_prefix+'_'+ m.hexdigest() + '.raw'
		
	def check_cache(self,message):
		name=self.cachefile_name(message)
		if (os.path.exists(name)):
			f=open(name)
			data=f.read()
			f.close()
			return data
		else:
			return None
	
	
	
	def cache(self,message,data):
		name=self.cachefile_name(message)
		f=open(name,'a')
		f.write(data)
		f.close()