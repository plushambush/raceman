from circuits import handler,Component,Event
import socket
from raceman.lib.config import *
from raceman.lib.sound_base import *
from raceman.lib.tts_base import *
import pdb

class RMTTS_SAPI(RMTTS):
	cache_prefix='SAPI'
	@handler("RMTTSConvertMessage")
	def rmtts_sapi_convert_message(self,message,rmprio=RM_PRIO_NORMAL):
		msg=self.check_cache(message)
		if (not msg):
			sock=socket.socket()
			sock.connect((TTS_SAPI_SERVER_HOST,TTS_SAPI_SERVER_PORT))
#		pdb.set_trace()
			sock.send(("%s\r\n" % message).encode('windows-1251'))
	
			msg=''
			while True:		
				data=sock.recv(TTS_SAPI_BUFFER_SIZE)
				if data<>'':
					msg=msg+data
				else:
					break
			sock.close()
			if len(msg)>0:
				self.cache(message,msg)
		if len(msg)>0:
			self.fireEvent(RMSoundPlayBuffer(bytearray(msg),rmprio))