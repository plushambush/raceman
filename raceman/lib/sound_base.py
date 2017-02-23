# Basic RMSound events
from circuits import Event,Component
from raceman.lib.eventqueue import *
from raceman.lib.prio import *
from raceman.lib.tts_base import *
import raceman.lib.config as config
from raceman.lib.config import *
import pdb

class RMSoundDriverInit(Event):
	"""Initialize sound driver
	Parameters:
		none
	"""
	success=True

class RMSoundDriverPlayStreamSync(Event):
	"""Play audiostream (sync)
	Parameters:
		datastream(string) - a stream to be played
	"""
	complete=True
	pass
		
class RMSoundDriverPlayStreamAsync(Event):
	"""Play audiostream (async)
	Parameters:
		datastream(string) - a stream to be played
	"""
	pass		
		
class RMSoundDriverPlayFileSync(Event):
	"""Play audiofile (sync)
	Parameters:
		filename - name of the file to be played
	"""
	complete=True
	pass

class RMSoundDriverPlayFileAsync(Event):
	"""Play audiofile (async)
	Parameters:
		filename - name of the file to be playes
	"""
	pass	
	
	
class RMSoundDriverPlayBufferSync(Event):
	"""Play audiobuffer (sync)
	Parameters:
		buffer - buffer to be played
	"""
	complete=True
	pass

class RMSoundDriverPlayBufferAsync(Event):
	"""Play audiobuffer (async)
	Parameters:
		buffer - buffer to be played
	"""
	pass	
	
	
	
class RMSoundDriverPlayBGM(Event):
	"""Play background music
	Parameters:
		filename(string) - name of the file to be played
	"""
	pass
	
class RMSoundDriverStopBGM(Event):
	"""Stop background music
	Parameters:
		none
	"""	
	pass
	
class RMSoundDriverStopAll(Event):
	"""Stop all sound
	Parameters:
		none
	"""
	pass


class RMSoundSayMessage(Event):
	"""Say a message via TTS
	Parameters:
		message(string) - a message to be played
	"""
	pass
	
	
class RMSoundPlayFile(Event):
	pass	
	

class RMSoundPlayStream(Event):
	pass	

class RMSoundPlayBuffer(Event):
	pass

class RMSoundPlayFileOOB(Event):
	pass
	
class RMSoundPlayStreamOOB(Event):
	pass
	
	
class RMSoundPlayBGM(Event):
	pass
	
	
class RMSoundStopBGM(Event):
	pass	

	
def SoundFullPath(sound):
	return RMS_SOUND_DIR+'/'+config.profile['RMS_SOUND_THEME']+'/'+sound	
	
	
class RMSound(Component):
	def __init__(self,*args,**kwargs):
		super(RMSound,self).__init__(args,kwargs)
		self._bus=self.__class__.__name__
		self.SoundQ=EventQueue(channel=self._bus).register(self)
		self.SoundQH=EQHandler(channel=self._bus).register(self)

	@handler("started")
	def _on_started(self,komponent):
		self.fireEvent(RMSoundDriverInit(),self._bus)
		
	@handler("RMSoundDriverInit_success")
	def _on_rmsound_driver_init_success(self,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(),self._bus)
		
	@handler("RMSoundPlayFile")
	def _on_rmsound_play_file(self,filename,rmprio=RM_PRIO_NORMAL):
		if filename<>'':
			self.fireEvent(EQEnqueueEvent(RMSoundDriverPlayFileSync(SoundFullPath(filename)),rmprio),self._bus)

	@handler("RMSoundDriverPlayFileSync_complete")
	def _on_rmsound_driver_play_file_sync_complete(self,event,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(),self._bus)

	@handler("RMSoundPlayStream")
	def _on_rmsound_play_stream(self,stream,rmprio=RM_PRIO_NORMAL):
		self.fireEvent(EQEnqueueEvent(RMSoundDriverPlayStreamSync(stream),rmprio),self._bus)

	@handler("RMSoundDriverPlayStreamSync_complete")
	def _on_rmsound_driver_play_stream_sync_complete(self,event,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(),self._bus)

	@handler("RMSoundPlayBuffer")
	def _on_rmsound_play_buffer(self,buffer,rmprio=RM_PRIO_NORMAL):
		self.fireEvent(EQEnqueueEvent(RMSoundDriverPlayBufferSync(buffer),rmprio),self._bus)

	@handler("RMSoundDriverPlayBufferSync_complete")
	def _on_rmsound_driver_play_buffer_sync_complete(self,event,*args,**kwargs):
		self.fireEvent(EQHandlerAvailable(),self._bus)




	@handler("RMSoundSayMessage")
	def on_rmsound_say_message(self,message,rmprio=RM_PRIO_NORMAL):
		self.fireEvent(RMTTSConvertMessage(message,rmprio))

	@handler("RMSoundPlayBGM")
	def _on_rmsound_play_bgm(self,filename):
		if filename<>'':
			self.fireEvent(RMSoundDriverPlayBGM(SoundFullPath(filename)))
		
	@handler("RMSoundStopBGM")
	def _on_rmsound_stop_bgm(self):
		self.fireEvent(RMSoundDriverStopBGM())
		
	@handler("RMSoundStopAll")
	def _on_rmsound_stop_all(self):
		self.fireEvent(RMSoundStopAll())
		
		